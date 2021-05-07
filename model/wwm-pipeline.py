from transformers import pipeline, AutoModelForMaskedLM, AutoTokenizer
from transformers.pipelines.fill_mask import FillMaskPipeline
from typing import TYPE_CHECKING, Optional, Union
import torch

class MultiMaskFilling(FillMaskPipeline):

    def __call__(self, *args, targets=None, top_k: Optional[int] = None, **kwargs):
        """
        Fill the masked token in the text(s) given as inputs.

        Args:
            args (:obj:`str` or :obj:`List[str]`):
                One or several texts (or one list of prompts) with masked tokens.
            targets (:obj:`str` or :obj:`List[str]`, `optional`):
                When passed, the model will return the scores for the passed token or tokens rather than the top k
                predictions in the entire vocabulary. If the provided targets are not in the model vocab, they will be
                tokenized and the first resulting token will be used (with a warning).
            top_k (:obj:`int`, `optional`):
                When passed, overrides the number of predictions to return.

        Return:
            A list or a list of list of :obj:`dict`: Each result comes as list of dictionaries with the following keys:

            - **sequence** (:obj:`str`) -- The corresponding input with the mask token prediction.
            - **score** (:obj:`float`) -- The corresponding probability.
            - **token** (:obj:`int`) -- The predicted token id (to replace the masked one).
            - **token** (:obj:`str`) -- The predicted token (to replace the masked one).
        """
        inputs = self._parse_and_tokenize(*args, **kwargs)
        outputs = self._forward(inputs, return_tensors=True)

        results = []
        batch_size = outputs.shape[0] if self.framework == "tf" else outputs.size(0)

        if targets is not None:
            if len(targets) == 0 or len(targets[0]) == 0:
                raise ValueError("At least one target must be provided when passed.")
            if isinstance(targets, str):
                targets = [targets]

            targets_proc = []
            for target in targets:
                target_enc = self.tokenizer.tokenize(target)
                if len(target_enc) > 1 or target_enc[0] == self.tokenizer.unk_token:
                    logger.warning(
                        f"The specified target token `{target}` does not exist in the model vocabulary. "
                        f"Replacing with `{target_enc[0]}`."
                    )
                targets_proc.append(target_enc[0])
            target_inds = np.array(self.tokenizer.convert_tokens_to_ids(targets_proc))

        for i in range(batch_size):
            input_ids = inputs["input_ids"][i]
            result = []
            
            masked_index = torch.nonzero(input_ids == self.tokenizer.mask_token_id, as_tuple=False)

            logits = outputs[i, masked_index.view(-1), :]
            probs = logits.softmax(dim=-1)
            if targets is None:
                values, predictions = probs.topk(top_k if top_k is not None else self.top_k)
            else:
                values = probs[..., target_inds]
                sort_inds = list(reversed(values.argsort(dim=-1)))
                values = values[..., sort_inds]
                predictions = target_inds[sort_inds]

            for v, p in zip(values.T.tolist(), predictions.T.tolist()):
                result.append(
                    {
                        "score": v,
                        "token": p,
                        "token_str": self.tokenizer.decode(p),
                    }
                )

            # Append
            results += [result]

        if len(results) == 1:
            return results[0]
        return results

if __name__ == '__main__':

    model_type='distilroberta-base'
    model=AutoModelForMaskedLM.from_pretrained(model_type)
    tokenizer=AutoTokenizer.from_pretrained(model_type)

    nlp=MultiMaskFilling(model, tokenizer)
    print(nlp('I <mask> <mask> you.'))