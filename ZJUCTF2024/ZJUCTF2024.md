# Result

- Total Rank: 115/382
- Group Rank: 57/188
- Score: 525
	- Misc: 125
	- Crypto: 125
	- Web: 125
	- Welcome: 150
- Solved Questions: 6 

# Welcome

etc.(for check-in, container instruction, check-out)

# Misc

## Minec(re)tf

1. `/tick freeze`以逃避限制
2. `map`文件夹中暴力搜索`flag`发现`flag_look_at_the_code_of_the_recipe.json`，获得piece1及hint
3. 对所有function添加指令以确认具体执行函数，由hint获得piece2、3
4. 据hint拆包mod，由`net\entityCatPig\testmod\entity\TestMobEntity.class`中获得`mask lore decrypt`获得piece5
5. 于大厅旁命令方块塔发现tag`received_reward`并去除，获得piece7
6. 据hint加载`gold_smith`结构，获得piece8
7. 据hint搜索`key card`发现`check_key_card.json`，针对此predicate搜索，获得piece9
8. 据hint在`resources.zip`中发现修改日期及命名异常的`lightblue_wool.json`，使用`blockbench`打开，获得piece4
9. piece6似了

## 小A口算

`pwntools+copilot`，程序未留档

# Crypto

## Shad0wTime

?

# Web

## easy Pentest

使用`OSS browser`直接访问，获得flag
