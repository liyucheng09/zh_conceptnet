# 中文Conceptnet

## 版本-特性

### v1.0

- `madarin_conceptnet_v10.csv` 完整版
- `madarin_conceptnet_solid_v10.csv` solid版
- `zh_conceptnet_v10.csv` 未转换原始版，包含繁体中文。

*solid版只取了可靠数据源的conceptnet edges。去掉了从游戏中自动生成的边（质量很差）。*

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

- 

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


## OMCS

OMCS的格式如下：

```
安全帽 可以用  塑膠 製成。
安全帽 可以用  絨布 製成。
你會  吃藥 因為你  生病了。
太潮濕 會讓你想要  不舒服 。
```