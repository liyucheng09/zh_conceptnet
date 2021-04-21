# TODO

- concept列表在`embeddings/concept.txt`里，关系列表在`embeddings/relation.txt`里。根据这个构建`concept-to-id`和`relation-to-id`两个字典。注意，relation字典只有17个关系，但是处理好的path文件中共有34种关系，这是因为关系反着来和正着来index是不一样的，所以映射时注意这一点。
- 处理好的问题在`datasets/csqa_new/train_rand_split.jsonl.statements.mcp`中，只看前40个即可。
- 处理好的路径在`datasets/csqa_new/train_rand_split.jsonl.statements.mcp.cls.pruned.0.15.json`中，只有前40个问题的对应路径。该文件里所有节点和关系都是用其对应的index表示的。

## 下一步

看看怎么生成路径对应的自然语言。

# 备忘录

Query: c1, c2, c3
Answer: c4,  c5

C1->c4, c2->c4, ...c1->c5, ...

- [x] Grounding: space.matcher
- [x] Pruning: 剪枝
- [x] Path-finding: networkx
- [x] Path-scoring: transE.
    - [ ] How, where, what, who
    - [ ] Relation type
- [x] Path-pruning

- [ ] Path 2 text: c1->c4,
    - [ ] Template

- [ ] Model
    - [ ] BERT
    - [ ] T5
