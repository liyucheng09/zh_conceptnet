# 中文Conceptnet

## 版本-特性

### v1.0

- `madarin_conceptnet_v10.csv` 完整版
- `madarin_conceptnet_solid_v10.csv` solid版
- `zh_conceptnet_v10.csv` 未转换原始版，包含繁体中文。
- `zh_omcs.csv` 中文版omcs

*solid版只取了可靠数据源的conceptnet edges。去掉了从游戏中自动生成的边（质量很差）。*

# TODO LIST

1. 处理omcs，得到模版


# 讨论区

## 常识知识的可能的来源

- 百科全书式的页面并不是理想的常识知识来源。
  - 例如，百科的「太阳」页面，包含了太阳的一系列数字，定义等等。这些不应作为常识存在。
- 常识应该为大多数人生活中经历的，实践中体验到的，感受和认识。
  - 例如：下雨天会淋湿，淋湿了容易感冒，感冒了会流鼻涕。
- 常识不应该是一成不变的
  - 如上文所述，常识来源与实践。那么常识按照人群应有差别
  - 例如：对于财经新闻的读者，基本的常识则包括与之相关的一系列知识。对于病历，应有基本医学常识等。
- Conceptnet的目的是？
  - 不追求涉及到所有的领域的所有的具体知识，只要求包含大多数人所了解的，所经历/体验过的常识信息

## 图谱扩建实现方式

### 分析

- 常识信息和知识信息相比，更不容易发生变化。所以说常识图谱不太需要周期性更新。
- 常识信息的来源和百科信息要有所区别。
- 从文本中发现的方法，应该和现有的抽取<实体，关系>三元组的方法有所区别。（因为常识信息的节点不一定是实体）

### 翻译

**TODO**

### 从文本中寻找

**TODO**


# 会议记录

## 01/14

### OMCS

**V1**
1. 网站给出一些activities，标注人员根据情况给出无模版的自然语言常识
   1. 例如，网站给出一短故事，标注人员给出帮助机器理解该故事的常识自然语言。
2. omcs网站共搜集了大约9000条常识文本

**V2**
1. 研究者根据V1得到的结果，抽取并选择了一些合适的模版。
2. 网站同样给出activities，标注者需要选择模版，填充模版。
3. 网站根据标注者填写的模版，联想新的模版，返回给用户，请其判断正误。
   1. 例如：妈妈有宝宝。我的房子。妈妈能生宝宝。-> 我能生房子。
4. 鼓励标注者使用常用词
5. 标注者和算法共同消岐
6. 人工标注，判断omcs的质量

## 01/17

### ConceptNet 2.0

conceptnet2.0《ConceptNet — a practical commonsense reasoning tool-kit》

1. 和WordNet、Cyc的区别：
   1. WordNet致力于词汇分级、单词相似度的判定；节点是一个单词或短语，由自然语言表示；易使用
   2. Cyc致力于正式的逻辑推理；节点用特定的逻辑描述来表示，有自己的CycL语言；不易使用
   3. ConceptNet致力于在文本中能够做出实际的、基于上下文的推理；节点是复合型概念，自然语言表示；易使用
2. 构建ConceptNet 
   1. 采用约50条抽取规则将OMCS半结构的句子转换成二元关系断言
      1. 用20种关系（**TODO**除了ThematicKLine关系和SuperThematicKLine关系？），采用正则表达式将句子变成断言
      2. 没有合适的对应关系的句子用“ConceptuallyRelatedTo”kline关系表示；
      3. 节点是复合型的，由动词、名词短语、介词短语和形容词短语构成。
   2. Normalisation阶段
      1. 修改错误拼写、节点符合句法约束、去掉停用词、is/are/were→be、复数变单数…
3. Relaxation阶段
   1. 去重；
   2. 用启发性找出更一般的断言（如果children nodes都有那么parent node也有）；不建议使用
   3. 构造SuperThematicKLine关系，使更具体的关系转为更泛华的，这样有助于构建节点的连接。；
   4. 如果节点的名词短语中有形容词短语修饰，这个特性也可以上升到父节点；
   5. 解决Vocabulary differences（如bike/bicycle）和Morphological variations（如relax/relaxation）


### 计划

1. 从omcs中文文本中抽取文本模版：例如：Noun 可以用  Noun 製成。 -> <Noun，Madeof，Noun>
2. **选定合适的数据源**，根据1）中抽取的文本模版，匹配内容。
   1. 合适的数据源应与知识图谱的数据源做出区分，应与常识知识相符
   2. *应兼顾普遍性常识与专业领域常识*
   3. 匹配内容应选择/或设计合适的算法
3. **验证** 2）中得到的edges，此处应设计合适的算法。最好应结合整个图来推断。
4. **消岐**，简化。
5. 根据1，2，3）得到的初步常识图谱，设计算法，*完善*该图谱
   1. 完善的过程包括去掉冗余的边，增加应添加的边。
6. *应为每个edge打上领域标签，以适应通用任务和领域任务。*
7. 使用常识图谱，生成中文常识问答数据集。以验证中文NLP模型的常识知识水平。



# 参考资料

- Does BERT Solve Commonsense Task via Commonsense Knowledge?
  - 使用conceptnet验证了BERT包含常识知识。
- COMMONSENSEQA: A Question Answering Challenge Targeting Commonsense Knowledge
  - CommensenseQA，根据conceptnet构建的常识问答数据库，选择题的形式。可以帮助理解他人眼中的常识是什么样子的.
- `CommensenseQA`数据集：百度网盘
- 百度，清华提出的基于知识图谱增强的BERT：https://zhuanlan.zhihu.com/p/75466388
- CommonGen: A Constrained Text Generation Challenge for Generative Commonsense Reasoning
  - 需要常识知识的生成任务
- 微软probase概念图谱：https://concept.research.microsoft.com/Home/Introduction
- OMCS：OMCS是conceptnet的数据来源，换句话说，conceptnet是从OMCS数据中解析得来的。
  - http://courses.csail.mit.edu/6.803/pdf/openmind.pdf
  - **TODO** 看论文，明确两个问题：
    - OMCS的标注流程是什么。（是否有输入，输出是什么）
    - 具体来说，如何从OMCS的预料中抽取出conceptnet的结构的（正则？还是信息抽取技术？）。
- Conceptnet2.0：http://alumni.media.mit.edu/~hugo/publications/papers/BTTJ-ConceptNet.pdf
  - project地址：http://alumni.media.mit.edu/~hugo/conceptnet/
  - python包：https://pypi.org/project/ConceptNet/


## OMCS

OMCS的格式如下：

```
安全帽 可以用  塑膠 製成。
安全帽 可以用  絨布 製成。
你會  吃藥 因為你  生病了。
太潮濕 會讓你想要  不舒服 。
```