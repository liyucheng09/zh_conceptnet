user_dict=['南京', '南京市', '长江', '大桥', '江大桥']
sentence='南京市长江大桥'
results=[]

def tokenize(sentence):
    i=0
    while i <len(sentence):
        start=i
        end=len(sentence)
        while end>start:
            if sentence[start:end] in user_dict:
                results.append(sentence[start:end])
                i=end
                print(start, '-' ,end)
                break
            else:
                end-=1
                print(start, '*', end)
    return results

print(tokenize(sentence))