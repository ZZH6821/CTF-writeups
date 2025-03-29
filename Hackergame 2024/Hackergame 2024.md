# Result

- Score: 1550
  - AI: 0
  - binary: 0
  - general: 850
  - math: 550
  - web: 150
- Total Rank: 408/2460
- ZJU Group Rank: 21/44

# Web

## Check-in

尝试任意提交，观察到提交失败所得网址中 `pass=false` ，将其改为 `pass=true` ，得到 flag `flag{w31ComE-tO-h@CKerG4me-aNd-enJOY-h@ckiN9-Zoz4}`

## 喜欢做签到的 CTFer 你们好呀

由 hint 进入 `nebuu.la` ，输入 `env` 后得到 flag1(Checkin Again) `flag{actually_theres_another_flag_here_trY_to_f1nD_1t_y0urself___join_us_ustc_nebula}`
输入 `ls -a` 后发现 `.flag` ，尝试打开无果，于源码中暴力搜索 `flag` ，发现 base64 编码的`ZmxhZ3swa18xNzVfYV9oMWRkM25fczNjM3J0X2YxNGdfX19wbGVhc2Vfam9pbl91c191c3RjX25lYnVsYV9hbkRfdHdvX21hSm9yX3JlcXVpcmVtZW50c19hUmVfc2hvd25fc29tZXdoZXJlX2Vsc2V9` ，
解码得 flag2(Checkin Again & Again) `flag{0k_175_a_h1dd3n_s3c3rt_f14g___please_join_us_ustc_nebula_anD_two_maJor_requirements_aRe_shown_somewhere_else}`

# General

## 打不开的盒

使用任意工具打开 stl 文件，得到模型内部的 flag `flag{Dr4W_Us!nG_fR3E_C4D!!w0W}`

## 猫咪问答（Hackergame 十周年纪念版）

1. 在 Hackergame 2015 比赛开始前一天晚上开展的赛前讲座是在哪个教室举行的？（30 分）
   于 `lug.ustc.edu.cn/wiki/lug/events/hackergame` 中找到 Hackergame 2015 活动记录，得到答案**_3A204_**
2. 众所周知，Hackergame 共约 25 道题目。近五年（不含今年）举办的 Hackergame 中，题目数量最接近这个数字的那一届比赛里有多少人注册参加？（30 分）
   查阅过往活动可知，题目数量最接近这个数字的为 Hackergame 2018（28 道），由对应活动记录得到答案**_2682_**
3. Hackergame 2018 让哪个热门检索词成为了科大图书馆当月热搜第一？（20 分）
   于 Hackergame 2018 猫咪问答官方题解及 repo `misc/others.md` 中，得到答案**程序员的自我修养**
4. 在今年的 USENIX Security 学术会议上中国科学技术大学发表了一篇关于电子邮件伪造攻击的论文，在论文中作者提出了 6 种攻击方法，并在多少个电子邮件服务提供商及客户端的组合上进行了实验？（10 分）
   搜索得新闻稿，确认论文为*FakeBehalf: Imperceptible Email Spoofing Attacks against the Delegation Mechanism in Email Systems*，利用 AI 阅读，得到答案**_336_**
5. 10 月 18 日 Greg Kroah-Hartman 向 Linux 邮件列表提交的一个 patch 把大量开发者从 MAINTAINERS 文件中移除。这个 patch 被合并进 Linux mainline 的 commit id 是多少？（5 分）
   易知为` Commit 6e90b67` ，得到答案**_6e90b6_**
6. 大语言模型会把输入分解为一个一个的 token 后继续计算，请问这个网页的 HTML 源代码会被 Meta 的 Llama 3 70B 模型的 tokenizer 分解为多少个 token？（5 分）
   利用 token counter 所得数字在 1835-1836 左右，尝试得到答案**_1833_**
   60 分对应 flag1(喵？)`flag{@_9O0D_CA7_i$_THe_caT_Who_©4n_PαS$_THE_qบ12}`
   100 分对应 flag2(喵！)`flag{t3И_Y3αR5_ØF_H@cK3Я9AMe_oMEDEt0บ_ω!tH_neKO_Qu!z}`

## 旅行照片 4.0

1.  照片拍摄的位置距离中科大的哪个校门更近？（格式：`X校区Y门`，均为一个汉字）
    搜索**科里科气科创驿站**，由地图得到答案**_东校区西门_**
2.  话说 Leo 酱上次出现在桁架上是……科大今年的 ACG 音乐会？活动日期我没记错的话是？（格式：`YYYYMMDD`）
    B 站搜索**中科大 LEO 动漫协会**，查找相关视频，易得答案**_20240519_**
    Q1-2 得到 flag1(LEO_CHAN?) `flag{5UB5CR1B3_T0_L30_CH4N_0N_B1L1B1L1_PLZ_6f061d8e1d}`
3.  这个公园的名称是什么？（不需要填写公园所在市区等信息）
    发现垃圾桶上**六安园林**标识，搜索六安境内公园尝试，得到答案**_中央公园_**
4.  这个景观所在的景点的名字是？（三个汉字）
    `google`识图匹配，得到答案**_坛子岭_**
    Q3-4 得到 flag2(FULL_RECALL) `flag{D3T41LS_M4TT3R_1F_R3V3RS3_S34RCH_1S_1MP0SS1BL3_a6d024d03e}`
5.  距离拍摄地最近的医院是？（无需包含院区、地名信息，格式：XXX 医院）
    由 hint 搜索**四编组动车组**，得**CRH6F-A**、**CRH6A-A**两车型，
    查阅 `china-emu.cn` 发现 CRH6F-A 页面头图**怀密号**符合题图中动车组涂装，经查询得其运行于怀密线，停放于**北京北动车所**，
    对照地图确认题图拍摄于**积水潭医院**楼顶，得到答案**_积水潭医院_**
6.  左下角的**动车组型号**是？
    如上所述，左下动车组与图中上动车组均为 CRH6F-A，得到答案**_CRH6F-A_**
     Q5-6 得到 flag3(OMINOUS_BELL) `flag{1_C4NT_C0NT1NU3_TH3_5T0RY_4NYM0R3_50M30N3_PLZ_H3LP_5ccfd57117}`

## 每日论文太多了！

下载论文 pdf，搜索 `flag` 发现被白色色块掩盖的**flag here**，得到 flag `flag{h4PpY_hAck1ng_3veRyd4y}`

# Math

## 零知识数独(1/3)

解数独，得到 flag1(数独高手) `flag{SUD0KU_M45T3R_You_Have_Shown_Y0ur_Know1edge_ac5207a9}`

## 惜字如金 3.0(1/3)

题目 A：

```python
bas64->base64
r->re
asert->assert
rang->range
els->else
litl->little
IGNORECAS->IGNORECASE
__fil__->__file__
encod->encode
writ->write
apend->append
remov->remove
FileNotFoundEror->FileNotFoundError
pas->pass
__nam__->__name__
Respons->Response
content_typ->content_type
enumerat->enumerate
Non->None
```

得到 flag1(题目 A) `flag{C0mpl3ted-Th3-Pyth0n-C0de-N0w}`

## 关灯(3/4)

copilot 编写[程序](1-3.py)，得到 flag1(Easy) `flag{bru7e_f0rce_1s_a1l_y0u_n3ed_bcb9e64a31}` ，
flag2(Medium) `flag{prun1ng_1s_u5eful_14533a5c90}` ，
flag3(Hard) `flag{lin3ar_alg3bra_1s_p0werful_64d7b6c1da}`
