#import opencc
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


def normalize_dataframe(one_line):
    """

    对conceptnet进行归一化。

    使用方法：
    将conceptnet的csv文件转地方成dataframe对象；然后
    df=df.apply(normalize_dataframe, axis=1)

    """
    url, rel, start, end, edge_info = one_line
    start=start.strip('/c/zh/')
    end=end.strip('/c/zh/')
    rel=rel.strip('/r/')
    
    start=start if '/' not in start else start.split('/')[0]
    url=rel+','+start+','+end

    if rel=='Synonym' and start==end:
        return pd.Series({'url': pd.NA, 'start':pd.NA, 'rel':pd.NA, 'end':pd.NA})

    return pd.Series({'url': url, 'start':start, 'rel':rel, 'end':end})


def get_all_nodes(df: pd.DataFrame):
    """

    df: 已经归一化后的conceptnet的dataframe对象
    返回conceptnet的所有节点

    """
    nodes=pd.concat([df['start'], df['end']])
    return nodes.drop_duplicates()

def simplify_omcs(omcs_csv_file_path):
    """
    简体化omcs数据库。
    输入是omcs_csv文件的路径
    返回汉化后的omcs dataframe
    """
    converter=opencc.OpenCC('tw2sp')
    def process_one_line(line):
        text=line['text']
        creator_id=line['creator_id']
        activity_id=line['activity_id']

        text=converter.convert(text)

        return pd.Series({
            'text':text,
            'creator_id':creator_id,
            'activity_id':activity_id
        })
    df=pd.read_csv(omcs_csv_file_path, index_col=0)
    return df.apply(process_one_line, axis=1)


def get_template_from_omcs(simplified_omcs_csv_path):
    """
    从omcs中获取模板
    输入是汉化后的simplified_omcs.csv文件的路径
    返回抽出的模板+没法抽模板的句子 template_sentence_csv
    """
    template_log_id = []
    template_temp = []
    template = []
    nodes = []

    df=pd.read_csv(zh_omcs_csv_path)
    text = df[['id','text']].values.tolist()
    #print(text)
    for id,value in text:
        b = ''
        c = ''
        #print(value)
        if value[0]==' ':
            a = value[0:value.find(' ',2)]
            value = value.replace(value[0:value.find(' ',2)+1], '_')  # "_可以用  叶子 制成。"
        temp = value[value.find('  '):]  #"  叶子 制成。"
        #if temp=='。':
            #num+=1
            #print({id:temp})
        if temp!='。':   #193649条
            b = temp[:temp.find(' ',3)]  #"  叶子"
            value = value.replace(b, '_')
            temp2 = value[value.find('  '):]
            if temp2!='。':
                c = temp2[:temp2.find(' ',3)] 
                value = value.replace(c, '_')
            nodes.append({id : [a , b , c]})
        template_log_id.append({id : value})
        template_temp.append(value)
    df_template = pd.DataFrame(template_temp, columns=['template']) 
    return df_template.drop_duplicates()
    
def get_template_from_template_sentence(template_sentence_csv_path):
    df=pd.read_csv(template_sentence_csv_path)
    template = df[['template']].values.tolist()[:35]
    sentences = df[['template']].values.tolist()[35:]
    print(sentences)
    # template = df

def get_en_omcs(simplified_omcs_file_path):
    df=pd.read_csv(simplified_omcs_file_path,sep='\t',error_bad_lines=False)
    df = df[df['language_id']=='en']
    a = 1
    for id, sub_df in df.groupby('activity_id'):
        print(id,len(sub_df.index))
        #sub_df.to_csv(str(id)+'.csv')
    



if __name__=='__main__':
    df= get_template_from_template_sentence('../../Data/template_from_omcs.csv')
    #df.to_csv('en_omcs.csv')
    