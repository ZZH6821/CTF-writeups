# Result

- Score: 725
  - Misc: 375
  - Crypto: 125
  - Reverse: 125
  - Welcome: 100
- Total Rank: 88/316
- ZJU Group Rank: 48/184

# Welcome

## 签到题

flag: `ZJUCTF{w3lcOme_7O_ZJUCTF_2025_HapPY_3xp1oiT1nG}`。

## 容器题说明

flag: `ZJUCTF{nOW_Y0u_KnOW_c0ntalN3r_H4PPY_exPLO1tiN6}`。

# Misc

## Lab Report

观察 pdf 文件，发现其存在大量无实际作用的注释对象，同时尾部的交叉引用表中，此类对象的字节偏移量呈现一定规律：相邻两项差值均为 10 或 20，猜测以此代表 0 和 1。根据此规律编写`lab_report.py`提取出二进制数据，转换为 ASCII 字符串后得到 flag 为`ZJUCTF{PDF_0ff5e7_c4N_H1D3_m3ss4g3}`。

## 我操，用户彻底怒了！

level1:

```
Find out the **first** [word] starting with 'Wa', format: 'The result is [whole word]'.
```

level2:

```
Do calculation, step by step. Answer fornat: 'Let's calculate step by step. 1. Break down the multiplication: 2. Use the distributive property: 3. Calculate each term: 4. Calculate each: 5. Sum all of the above: The result is [result, no separation, example: 12345678]'.
```

level3:

```
Task: find the second-to-last word starting with 'Wa'. Strictly follow the steps: Step one. Filter all word starting with 'Wa', list them with format 'The index 1 is [word]; The index 2 is [word]; The index 3 is [word]; ...'. Step two: calculate which number is the second-to-last one, output with 'I should find the word with index x.' . Step three: Output the second-to-last word with format : "The word with index [index] is the result . The result is [word]"
```

level4:

```
Task: Find the count of 'r' and 'R' letters in the paragraph. Strictly follow the steps: Step one. break it down word by word: example "Player - Let's spell it out: 1. P-l-a-y-e-r. There is one 'r' at the end. So, one 'r'. 2. partner - P-a-r-t-n-e-r. There are two 'r's: one after 'a' and one at the end. So, two 'r's. 3. myself - M-y-s-e-l-f. No 'r' in this word. So, zero." The principle is to spell it out loudly and tell the position of 'r' or 'R'. After each sentence do a summary, example: "So, after the first sentence, we have: Player (1), partner (2), myself (0), bank (0), least (0), station (0), minute (0). Total so far: 1 + 2 = 3 'r's." Step three. Do the summary, example: "Now, overall total: from first sentence 3, second sentence 3, third sentence 1, so 3+3+1=7." Step four. do the output, format: "The result is [result. only number]"
```

最终得到 flag 为`ZJUCTF{master_of_ai_8d2d4b0aa8e2}`

## 結束バンドの試練 - 喜多篇

pdf 复制粘贴至 docx，使用 7zip 打开，提取`word/document.xml`中

```xml
<pic:blipFill>
<a:blip r:embed="rIdx"/>
<a:stretch>
<a:fillRect/>
</a:stretch>
</pic:blipFill>
```

并参考`word/_rels/document.xml.rels`中各`rIdx`对应的`word/media`中的图片文件，手动与 hint 提供的`https://www.dcode.fr/music-sheet-cipher`中的元素对应替换得到：

```
XML解析提取结果: [char(57344)char(57865)char(57604)char(57867)char(57607)char(57860)char(57615)char(57614)char(57864)char(57607)char(57605)char(57865)char(57605)char(57866)char(57860)char(57610)char(57864)char(57860)char(57863)char(57870)char(57866)char(57614)char(57866)char(57605)char(57867)char(57613)char(57859)char(57868)char(57861)char(57603)char(57607)char(57607)char(57866)char(57606)char(57867)char(57866)char(57605)char(57616)char(57864)char(57866)char(57864)char(57612)char(57606)char(57866)char(57864)char(57607)char(57605)char(57614)char(57616)char(57859)char(57863)char(57604)char(57611)char(57616)char(57616)char(57862)char(57613)char(57862)char(57612)char(57610)char(57613)char(57608)char(57860)char(57870)char(57611)char(57603)char(57611)char(57861)char(57867)char(57865)char(57862)char(57867)char(57865)char(57612)char(57865)char(57610)char(57616)char(57609)char(57870)char(57616)char(57865)char(57861)char(57616)char(57607)char(57870)char(57867)char(57604)char(57870)char(57867)char(57607)char(57863)char(57611)char(57865)char(57859)char(57869)char(57869)char(57869)char(57612)char(57612)char(57607)char(57863)char(57868)char(57609)char(57867)char(57869)char(57864)char(57610)char(57867)char(57607)char(57603)char(57613)char(57867)char(57868)char(57865)char(57868)char(57867)char(57611)char(57615)char(57867)char(57610)char(57609)char(57866)char(57609)char(57616)char(57861)char(57613)char(57612)char(57614)char(57860)char(57605)char(57605)char(57868)char(57611)char(57860)char(57603)char(57607)char(57613)char(57863)char(57869)char(57610)char(57867)char(57609)char(57611)char(57865)char(57860)char(57861)char(57861)char(57869)char(57868)char(57607)char(57609)char(57605)char(57859)char(57603)char(57608)char(57613)char(57870)char(57611)char(57859)char(57615)char(57614)char(57612)char(57866)char(57612)char(57869)char(57603)char(57604)char(57608)char(57607)char(57604)char(57870)char(57865)char(57605)char(57862)char(57611)char(57867)char(57863)char(57864)char(57867)char(57606)char(57867)char(57610)char(57608)char(57612)char(57607)char(57868)char(57614)char(57869)char(57862)char(57869)char(57604)char(57860)char(57869)char(57604)char(57861)char(57867)char(57605)char(57862)char(57870)char(57606)char(57870)char(57612)char(57604)char(57859)char(57864)char(57861)char(57870)char(57867)char(57610)char(57616)char(57605)char(57603)char(57859)char(57860)char(57603)char(57859)char(57606)char(57605)char(57609)char(57605)char(57614)char(57866)char(57605)char(57606)char(57859)char(57605)char(57861)char(57606)char(57615)char(57607)char(57862)char(57869)char(57866)char(57863)char(57607)char(57862)char(57606)char(57860)char(57605)char(57608)char(57862)char(57615)char(57604)char(57870)char(57603)char(57612)char(57612)char(57616)char(57613)char(57614)char(57614)char(57613)char(57616)char(57862)char(57865)char(57864)char(57604)char(57604)char(57603)char(57860)char(57612)char(57615)char(57870)char(57867)char(57611)char(57609)char(57868)char(57870)char(57613)char(57866)char(57864)char(57870)char(57612)char(57869)char(57603)char(57860)char(57604)char(57605)char(57612)char(57610)char(57859)char(57861)char(57866)char(57870)char(57868)char(57869)char(57603)char(57610)char(57615)char(57613)char(57868)char(57603)char(57609)char(57615)char(57615)char(57616)char(57613)char(57864)char(57608)char(57869)char(57865)char(57860)char(57865)char(57870)char(57612)char(57616)char(57865)char(57863)char(57606)char(57606)char(57609)char(57606)char(57863)char(57865)char(57862)char(57868)char(57867)char(57606)char(57609)char(57860)char(57609)char(57870)char(57604)char(57870)char(57610)char(57870)char(57612)char(57861)char(57870)char(57870)char(57863)char(57859)char(57870)char(57614)char(57616)char(57609)char(57616)char(57616)char(57869)char(57610)char(57608)char(57865)char(57609)char(57604)char(57867)char(57605)char(57613)char(57864)char(57861)char(57606)char(57866)char(57866)char(57609)char(57864)char(57609)char(57616)char(57862)char(57611)char(57867)char(57605)char(57612)char(57612)char(57869)char(57868)char(57861)char(57607)char(57606)char(57616)char(57864)char(57612)char(57861)char(57606)char(57608)char(57859)char(57862)char(57866)char(57606)char(57613)char(57862)char(57610)char(57870)char(57614)char(57615)char(57859)char(57606)char(57614)char(57864)char(57614)char(57606)char(57607)char(57865)char(57868)char(57864)char(57862)char(57609)char(57611)char(57611)char(57609)char(57604)char(57613)char(57612)char(57867)char(57860)char(57867)char(57608)char(57607)char(57861)char(57869)char(57603)char(57870)char(57603)char(57859)char(57862)char(57870)char(57616)char(57870)char(57860)char(57860)char(57604)char(57607)char(57869)char(57869)char(57606)char(57862)char(57614)char(57604)char(57866)char(57606)char(57615)char(57605)char(57866)char(57864)char(57859)char(57867)char(57614)char(57860)char(57862)char(57608)char(57860)char(57611)char(57607)char(57866)char(57869)char(57859)char(57859)char(57610)char(57870)char(57605)char(57609)char(57613)char(57866)char(57865)char(57608)char(57608)char(57861)char(57612)char(57603)char(57605)char(57611)char(57615)char(57603)char(57862)char(57608)char(57605)char(57610)char(57608)char(57615)char(57611)char(57613)char(57867)char(57613)char(57612)char(57613)char(57868)char(57859)char(57866)char(57614)char(57614)char(57610)char(57608)char(57613)char(57606)char(57869)char(57603)char(57614)char(57867)char(57614)char(57865)char(57610)char(57865)char(57606)char(57615)char(57615)char(57868)char(57860)char(57607)char(57603)char(57607)char(57614)char(57605)char(57615)char(57605)char(57608)char(57607)char(57865)char(57870)char(57867)char(57610)char(57614)char(57615)char(57608)char(57870)char(57605)char(57869)char(57866)char(57867)char(57610)char(57860)char(57605)char(57609)char(57867)char(57605)char(57863)char(57615)char(57605)char(57616)char(57867)char(57863)char(57867)char(57870)char(57613)char(57607)char(57864)char(57859)char(57864)char(57615)char(57860)char(57865)char(57614)char(57861)char(57863)char(57605)char(57604)char(57863)char(57606)char(57604)char(57612)char(57612)char(57614)char(57610)char(57605)char(57868)char(57614)char(57859)char(57614)char(57612)char(57610)char(57862)char(57609)char(57863)char(57867)char(57608)char(57870)char(57606)char(57610)char(57615)char(57607)char(57869)char(57864)char(57614)char(57860)char(57616)char(57614)char(57611)char(57613)char(57603)char(57863)char(57863)char(57615)char(57615)char(57865)char(57607)char(57868)char(57608)char(57614)char(57863)char(57862)char(57607)char(57614)char(57603)char(57606)char(57867)char(57607)char(57868)char(57608)char(57867)char(57613)char(57604)char(57608)char(57861)char(57870)char(57859)char(57864)char(57616)char(57868)char(57614)char(57860)char(57865)char(57615)char(57608)char(57869)char(57859)char(57866)char(57607)char(57860)char(57613)char(57603)char(57859)char(57610)char(57615)char(57613)char(57606)char(57861)char(57611)char(57613)char(57870)char(57863)char(57604)char(57609)char(57613)char(57612)char(57867)char(57604)char(57870)char(57869)char(57613)char(57605)char(57603)char(57604)char(57609)char(57606)char(57865)char(57614)char(57860)char(57865)char(57609)char(57616)char(57867)char(57614)char(57612)char(57866)char(57612)char(57863)char(57869)char(57861)char(57869)char(57609)char(57610)char(57869)char(57611)char(57609)char(57603)char(57863)char(57864)char(57870)char(57607)char(57613)char(57614)char(57860)char(57614)char(57611)char(57861)char(57866)char(57615)char(57614)char(57613)char(57863)char(57609)char(57606)char(57609)char(57613)char(57867)char(57860)char(57866)char(57613)char(57860)char(57864)char(57607)char(57869)char(57616)char(57615)char(57863)char(57861)char(57608)char(57608)char(57614)char(57611)char(57610)char(57864)char(57861)char(57867)char(57864)char(57609)char(57864)char(57864)char(57869)char(57866)char(57605)char(57870)char(57865)char(57859)char(57867)char(57611)char(57616)char(57868)char(57609)char(57870)char(57607)char(57609)char(57605)char(57610)char(57865)char(57606)char(57864)char(57861)char(57866)char(57859)char(57606)char(57604)char(57863)char(57610)char(57860)char(57868)char(57614)char(57859)char(57613)char(57607)char(57866)char(57860)char(57606)char(57869)char(57610)char(57604)char(57606)char(57605)char(57606)char(57614)char(57604)char(57862)char(57612)char(57862)char(57865)char(57611)char(57605)char(57614)char(57615)char(57607)char(57604)char(57868)char(57604)char(57867)char(57862)char(57609)char(57610)char(57862)char(57615)char(57866)char(57869)char(57613)char(57863)char(57867)char(57611)char(57612)char(57611)char(57862)char(57609)char(57867)char(57606)char(57867)char(57866)char(57866)char(57867)char(57610)char(57870)char(57616)char(57604)char(57862)char(57609)char(57614)char(57611)char(57609)char(57611)char(57869)char(57870)char(57606)char(57607)char(57610)char(57862)char(57867)char(57604)char(57864)char(57612)char(57606)char(57866)char(57613)char(57607)char(57614)char(57860)char(57603)char(57864)char(57864)char(57615)char(57870)char(57869)char(57612)char(57606)char(57866)char(57613)char(57604)char(57859)char(57606)char(57606)char(57869)char(57615)char(57864)char(57608)char(57612)char(57606)char(57609)char(57863)char(57867)char(57610)char(57613)char(57604)char(57865)char(57869)char(57606)char(57866)char(57868)char(57868)char(57616)char(57870)char(57606)char(57870)char(57859)char(57605)char(57868)char(57608)char(57868)char(57608)char(57607)char(57868)char(57863)char(57608)char(57612)char(57859)char(57865)char(57609)char(57616)char(57616)char(57610)char(57605)char(57865)char(57607)char(57615)char(57612)char(57868)char(57608)char(57612)char(57859)char(57611)char(57608)char(57862)char(57610)char(57604)char(57606)char(57860)char(57859)char(57606)char(57609)char(57606)char(57611)char(57862)char(57859)char(57612)char(57864)char(57616)char(57867)char(57859)char(57611)char(57613)char(57615)char(57603)char(57870)char(57611)char(57615)char(57866)char(57604)char(57612)char(57612)char(57610)char(57616)char(57615)char(57867)char(57861)char(57609)char(57866)char(57867)char(57869)char(57861)char(57606)char(57860)char(57609)char(57610)char(57609)char(57869)char(57605)char(57615)char(57863)char(57604)char(57870)char(57607)char(57609)char(57612)char(57865)char(57867)char(57604)char(57861)char(57870)char(57864)char(57862)char(57859)char(57864)char(57605)char(57868)char(57604)char(57610)char(57862)char(57613)char(57605)char(57868)char(57870)char(57865)char(57607)char(57867)char(57605)char(57605)char(57867)char(57870)char(57614)char(57616)char(57604)char(57614)char(57604)char(57603)char(57862)char(57862)char(57616)char(57867)char(57611)char(57610)char(57616)char(57606)char(57615)char(57866)char(57607)char(57869)char(57860)char(57862)char(57605)char(57615)char(57615)char(57603)char(57604)char(57603)char(57615)char(57869)char(57610)char(57603)char(57605)char(57607)char(57613)char(57609)char(57614)char(57611)char(57607)char(57863)char(57863)char(57603)char(57609)char(57605)char(57608)char(57608)char(57612)char(57865)char(57615)char(57614)char(57613)char(57606)char(57615)char(57863)char(57615)char(57606)char(57613)char(57607)char(57604)char(57867)char(57870)char(57866)char(57611)char(57864)char(57867)char(57611)char(57869)char(57860)char(57862)char(57609)char(57867)char(57610)char(57861)char(57609)char(57615)char(57859)char(57862)char(57609)char(57859)char(57863)char(57604)char(57863)char(57867)char(57870)char(57616)char(57603)char(57864)char(57604)char(57867)char(57616)char(57865)char(57607)char(57865)char(57860)char(57604)char(57869)char(57860)char(57609)char(57612)char(57865)char(57603)char(57614)char(57607)char(57861)char(57607)char(57606)char(57608)char(57863)char(57611)char(57605)char(57606)char(57869)char(57861)char(57607)char(57867)char(57867)char(57859)char(57608)char(57870)char(57605)char(57610)char(57869)char(57603)char(57606)char(57616)char(57866)char(57870)char(57604)char(57616)char(57859)char(57864)char(57869)char(57616)char(57869)char(57865)char(57612)char(57612)char(57612)char(57610)char(57616)char(57614)char(57865)char(57611)char(57612)char(57610)char(57859)char(57862)char(57605)char(57615)char(57860)char(57861)char(57859)char(57606)char(57865)char(57863)char(57608)char(57613)char(57605)char(57603)char(57605)char(57612)char(57861)char(57859)char(57603)char(57604)char(57610)char(57613)char(57616)char(57615)char(57859)char(57610)char(57862)char(57613)char(57605)char(57867)char(57863)char(57860)char(57613)char(57615)char(57614)char(57868)char(57614)char(57603)char(57865)char(57612)char(57862)char(57870)char(57608)char(57609)char(57610)char(57868)char(57603)char(57865)char(57861)char(57603)char(57869)char(57870)char(57607)char(57608)char(57864)char(57607)char(57864)char(57605)char(57611)char(57865)char(57606)char(57603)char(57864)char(57869)char(57605)char(57861)char(57606)char(57606)char(57614)char(57607)char(57865)char(57862)char(57613)char(57615)char(57608)char(57603)char(57612)char(57604)char(57861)char(57613)char(57609)char(57616)char(57866)char(57608)char(57862)char(57607)char(57867)char(57861)char(57869)char(57869)char(57859)char(57861)char(57870)char(57606)char(57609)char(57604)char(57606)char(57608)char(57609)char(57616)char(57869)char(57613)char(57866)char(57614)char(57605)char(57612)char(57606)char(57613)char(57861)char(57868)char(57867)char(57607)char(57607)char(57865)char(57608)char(57861)char(57867)char(57616)char(57860)char(57865)char(57868)char(57860)char(57616)char(57606)char(57611)char(57614)char(57869)char(57608)char(57604)char(57859)char(57867)char(57615)char(57606)char(57604)char(57614)char(57603)char(57859)char(57862)char(57868)char(57609)char(57865)char(57870)char(57860)char(57861)char(57604)char(57869)char(57863)char(57609)char(57866)char(57609)char(57612)char(57860)char(57609)char(57860)char(57608)char(57864)char(57614)char(57860)char(57613)char(57605)char(57868)char(57863)char(57615)char(57862)char(57616)char(57868)char(57864)char(57870)char(57605)char(57866)char(57861)char(57860)char(57607)char(57615)char(57870)char(57613)char(57866)char(57610)char(57859)char(57608)char(57611)char(57609)char(57606)char(57870)char(57611)char(57604)char(57615)char(57863)char(57610)char(57863)char(57608)char(57612)char(57603)char(57865)char(57864)char(57863)char(57869)char(57614)char(57608)char(57865)char(57615)char(57612)char(57860)char(57608)char(57870)char(57610)char(57606)char(57604)char(57860)char(57611)char(57859)char(57612)char(57863)char(57868)char(57614)char(57611)]
```

解密得到：

```
UBWEPMLTECUCVPHTPSZVLVCWKOXQAEEVDWVCNTVTJDVTECLNOSBINNRKRJHKFPZIAIQWURWUJUHNGZNUQNEZWBZWESIUOYYYJJESXGWYTHWEAKWXUXWIMWHGVGNQKJLPCCXIPAEKSYHWGIUPQQYXEGCOAFKZIOMLJVJYABFEBZUCRIWSTWDWHFJEXLYRYBPYBQWCRZDZJBOTQZWHNCAOPAODCGCLVCDOCQDMERYVSERDPCFRMBZAJJNKLLKNRUTBBAPJMZWIGXZKVTZJYAPBCJHOQVZXYAHMKXAGMMNKTFYUPUZJNUSDDGDSURXWDGPGZBZHZJQZZSOZLNGNNYHFUGBWCKTQDVVGTGNRIWCJJYXQEDNTJQDFORVDKRHZLMODLTLDEUXTRGIIGBKJWPWFEQYAZAORZNZPPBEYYDRLBVDMCVTOWLPRFPIEVYOOHZCGKVUFFQJACIMARFCHFMIKWKJKXOVLLHFKDYALWLUHUDMMXPEAELCMCFEUZWHLMFZCYVWHPCGWCSMCNWSWZKETOTMPULQSCBSDBJJLHCXLOLJHRGSWFZDHMEYTLPNLIKASSMMUEXFLSRELADWEXFWKBFQZOTNXLPUMFYOVEPKAOHMKDQIKZSBGKJWBZYKCABGDULPUGNWLJVJSYQYGHYIGASTZEKLPLIQVMLKSGDGKWPVKPTEYNMSQFFLIHTQWTGTTYVCZUOWINXGZEGCHUDTQVODBSHPXLOKEVPDYHBDCDLBRJRUICLMEBXBWRGHRMVYKSWIJIRGWDWVVWHZNBRGLIGIYZDEHRWBTJDVKELPATTMZYJDVKBODDYMTFJDGSWHKBUYDVXXNZDZOCXFXFEXSFJOUGNNHCUEMJXFJOIFRHBDPODGDIROJTNWOIKMAZIMVBJJHNMWQGVWYQDPGHGYCMSBZEGJUWBQZTROTCXBHRKCXZUEWCCWZLNBLBARRNWIHNDMVEYPRCMMABAMYHACEKGLIESSAGCFFJUMLKDMSMDKEBWZVITWIYPRGWHQGMORGOSBSWZNATBWNUEUPBYPGJUALEQEDFSICDYQEWWOFZCHYADNVZBNOTYNYUJJJHNLUIJHORCMPQODUSFKCACJQOABHKNMOHRKCWSPKMLXLAUJRZFGHXAUQAYZEFTETCIUDATYCQDDLEURKMFAJBQKGNVFREWQYYOQZDGBDFGNYKVLCJDKQXWEEUFQWNPUXPNDILYFBOWMDBLAORXGUZPQBYSGVGJPGPFTLPKCXSMRNXTZCVQPEMZKVHOFIGDZIBMSHSFJAUTSYLFUMJPFZHDBPIOJSXLI
```

## Bingo

AI, flag 为`ZJUCTF{10110_00010_00111_01010_01010}`

# Crypto

## crypt-it

simply `openssl pkeyutl -decrypt -in flag.enc -out decrypted_flag.txt -inkey private_key.pem -pkeyopt rsa_padding_mode:oaep` to get the flag `ZJUCTF{RSA_encrypt_with_OAEP_is_secure!}`。

# Reverse

## hello-reverse

IDA 反编译注意到核心函数为`main_main`与`main_checkPassword`，根据反编译所得代码容易编写出`hello-reverse.py`，解得 flag 为`ZJUCTF{Hello_Let's_Reverse_2025🎉}`。
