import opencc
import pandas as pd

def get_zh_edges(source_csv, target_csv):
    def is_zh_edge(slots):
        node1, node2=slots[2], slots[3]
        language=[node1.split('/')[2], node2.split('/')[2]]

        return all([i=='zh' for i in language])

    with open(source_csv, encoding='utf-8') as f:
        with open(target_csv, 'w', encoding='utf-8') as f2:
            line=f.readline()
            while line !='':
                slots=line.split('\t')
                if is_zh_edge(slots): f2.write(line)
                line=f.readline()

def get_dataframe(csv_file):
    return pd.read_csv(csv_file, sep='\t', names=['url', 'rel', 'start', 'end', 'edge_info'])


if __name__=='__main__':
    get_dataframe('zh_conceptnet.csv')

    