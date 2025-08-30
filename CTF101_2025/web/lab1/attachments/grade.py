import requests
import json
import logging
import re

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("grade_debug.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class ZjuAm:
    """统一身份认证模块"""

    @staticmethod
    def get_sso_cookie(username, password, debug=True):
        """
        获取iPlanetDirectoryPro cookie
        参数:
            username: 学号
            password: 密码
            debug: 是否开启调试模式
        返回:
            iPlanetDirectoryPro cookie值，失败返回None
        """
        session = requests.Session()
        try:
            if debug:
                logger.info("开始获取SSO Cookie")
                logger.debug(f"用户名: {username}")
            # 第一步：获取登录页面和execution参数
            login_url = "https://zjuam.zju.edu.cn/cas/login"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }
            if debug:
                logger.debug(f"第一步：访问登录页面: {login_url}")
            response = session.get(
                login_url, headers=headers, allow_redirects=False, timeout=10
            )
            if debug:
                logger.debug(f"登录页面响应状态码: {response.status_code}")
            # 提取execution参数
            execution_match = re.search(
                r'name="execution" value="(.*?)"', response.text
            )
            if not execution_match:
                raise Exception("无法获取execution参数")
            execution = execution_match.group(1)
            if debug:
                logger.debug(f"获取到execution: {execution}")
            # 第二步：获取RSA公钥
            pubkey_url = "https://zjuam.zju.edu.cn/cas/v2/getPubKey"
            if debug:
                logger.debug(f"第二步：获取RSA公钥: {pubkey_url}")
            response = session.get(pubkey_url, timeout=10)
            if debug:
                logger.debug(f"公钥响应状态码: {response.status_code}")
            pubkey_data = response.json()
            modulus_str = pubkey_data.get("modulus")
            exponent_str = pubkey_data.get("exponent")
            if not modulus_str or not exponent_str:
                raise Exception("无法获取RSA公钥")
            if debug:
                logger.debug(f"获取到modulus: {modulus_str[:50]}...")
                logger.debug(f"获取到exponent: {exponent_str}")
            # 第三步：RSA加密密码
            try:
                mod_int = int(modulus_str, 16)
                exp_int = int(exponent_str, 16)
                # 将密码转换为十六进制
                pwd_bytes = password.encode("utf-8")
                pwd_hex = "".join(f"{b:02x}" for b in pwd_bytes)
                pwd_int = int(pwd_hex, 16)
                # RSA加密
                pwd_enc_int = pow(pwd_int, exp_int, mod_int)
                pwd_enc = f"{pwd_enc_int:0128x}"
                if debug:
                    logger.debug(f"密码加密成功，长度: {len(pwd_enc)}")
            except Exception as e:
                raise Exception(f"密码加密失败: {str(e)}")
            # 第四步：提交登录表单
            login_data = {
                "username": username,
                "password": pwd_enc,
                "execution": execution,
                "_eventId": "submit",
                "rememberMe": "true",
            }
            headers.update(
                {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Origin": "https://zjuam.zju.edu.cn",
                    "Referer": "https://zjuam.zju.edu.cn/cas/login",
                }
            )
            if debug:
                logger.debug("第三步：提交登录表单")
            response = session.post(
                login_url,
                data=login_data,
                headers=headers,
                allow_redirects=False,
                timeout=10,
            )
            if debug:
                logger.debug(f"登录提交响应状态码: {response.status_code}")
                logger.debug(f"响应cookies: {list(response.cookies.keys())}")
            # 检查是否获取到iPlanetDirectoryPro
            iplanet_cookie = None
            for cookie in response.cookies:
                if cookie.name == "iPlanetDirectoryPro":
                    iplanet_cookie = cookie.value
                    break
            if not iplanet_cookie:
                raise Exception("学号或密码错误")
            if debug:
                logger.debug(f"成功获取iPlanetDirectoryPro: {iplanet_cookie[:50]}...")
            logger.info("SSO Cookie获取成功")
            return iplanet_cookie
        except requests.exceptions.Timeout:
            logger.error("请求超时")
            return None
        except requests.exceptions.ConnectionError:
            logger.error("网络连接错误")
            return None
        except Exception as e:
            logger.error(f"获取SSO Cookie失败: {str(e)}")
            if debug:
                logger.debug(f"异常详情: {type(e).__name__}: {e}", exc_info=True)
            return None


class ZdbkClient:
    def __init__(self):
        self.session = requests.Session()
        self.jsessionid = None
        self.route = None
        self.logged_in = False

    def login_with_credentials(self, username, password, debug=True):
        """
        使用用户名密码登录教务系统
        参数:
            username - 学号
            password - 密码
        """
        if debug:
            logger.info("开始使用用户名密码登录教务系统")
        # 首先获取iPlanetDirectoryPro
        iplanet_cookie = ZjuAm.get_sso_cookie(username, password, debug)
        if not iplanet_cookie:
            logger.error("无法获取iPlanetDirectoryPro")
            return False
        # 然后使用iPlanetDirectoryPro登录教务系统
        return self.login(iplanet_cookie, debug)

    def login(self, iplanet_directory_pro_cookie, debug=True):
        """
        使用iPlanetDirectoryPro cookie登录教务系统
        参数: iplanet_directory_pro_cookie - 统一身份认证的cookie值
        """
        if debug:
            logger.info("开始登录教务系统")
            logger.debug(f"iPlanetDirectoryPro: {iplanet_directory_pro_cookie[:50]}...")
        try:
            # 第一步：访问CAS登录页面
            cas_url = "https://zjuam.zju.edu.cn/cas/login?service=https%3A%2F%2Fzdbk.zju.edu.cn%2Fjwglxt%2Fxtgl%2Flogin_ssologin.html"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Cookie": f"iPlanetDirectoryPro={iplanet_directory_pro_cookie}",
            }
            if debug:
                logger.debug(f"第一步：访问CAS登录页面: {cas_url}")
            response = self.session.get(
                cas_url, headers=headers, allow_redirects=False, timeout=10
            )
            if debug:
                logger.debug(f"CAS响应状态码: {response.status_code}")
                logger.debug(f"CAS响应头: {dict(response.headers)}")
            # 检查重定向location
            location = response.headers.get("location")
            if not location:
                raise Exception("无法获取重定向地址，iPlanetDirectoryPro可能无效")
            # 处理http到https的转换
            if location.startswith("http://"):
                location = location.replace("http://", "https://", 1)
            if debug:
                logger.debug(f"重定向地址: {location}")
            # 第二步：访问重定向地址获取教务系统的cookies
            response = self.session.get(location, allow_redirects=False, timeout=10)
            if debug:
                logger.debug(f"教务系统响应状态码: {response.status_code}")
                logger.debug(f"教务系统响应头: {dict(response.headers)}")
                logger.debug(
                    f"获取到的cookies: {[f'{cookie.name}={cookie.value}' for cookie in response.cookies]}"
                )
            # 提取JSESSIONID和route
            jsessionid_found = False
            route_found = False
            for cookie in response.cookies:
                if cookie.name == "JSESSIONID" and "/jwglxt" in getattr(
                    cookie, "path", ""
                ):
                    self.jsessionid = cookie.value
                    jsessionid_found = True
                    if debug:
                        logger.debug(f"获取到JSESSIONID: {self.jsessionid}")
                elif cookie.name == "route":
                    self.route = cookie.value
                    route_found = True
                    if debug:
                        logger.debug(f"获取到route: {self.route}")
            if not jsessionid_found:
                raise Exception("无法获取JSESSIONID")
            if not route_found:
                raise Exception("无法获取route")
            self.logged_in = True
            logger.info("登录成功")
            return True
        except Exception as e:
            logger.error(f"登录失败: {str(e)}")
            if debug:
                logger.debug(f"异常详情: {type(e).__name__}: {e}", exc_info=True)
            return False

    def get_transcript(self, xn="", xq="", zscjl="", zscjr="", debug=True):
        """
        获取成绩单数据
        参数:
            xn: 学年，默认 ""
            xq: 学期，默认 ""
            zscjl: 成绩段最小值，默认 ""
            zscjr: 成绩段最大值，默认 ""
            debug: 是否开启调试模式
        """
        if not self.logged_in or not self.jsessionid or not self.route:
            raise Exception("未登录或登录状态无效")
        if debug:
            logger.info("开始获取成绩单")
            logger.debug(
                f"查询参数 - 学年: {xn}, 学期: {xq}, zscjl: {zscjl}, zscjr: {zscjr}"
            )
        url = "https://zdbk.zju.edu.cn/jwglxt/cxdy/xscjcx_cxXscjIndex.html?doType=query&queryModel.showCount=5000"
        headers = {
            "Host": "zdbk.zju.edu.cn",
            "Origin": "https://zdbk.zju.edu.cn",
            "Referer": "https://zdbk.zju.edu.cn/jwglxt/cxdy/xscjcx_cxXscjIndex.html",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Cookie": f"JSESSIONID={self.jsessionid}; route={self.route}",
            "Connection": "keep-alive",
        }
        # 构建 POST 数据
        data = {"xn": xn, "xq": xq, "zscjl": zscjl, "zscjr": zscjr}
        if debug:
            logger.debug(f"请求URL: {url}")
            logger.debug(f"POST数据: {data}")
            logger.debug("请求头信息:")
            for key, value in headers.items():
                if key == "Cookie":
                    logger.debug(f"  {key}: {value[:50]}...")
                else:
                    logger.debug(f"  {key}: {value}")
        try:
            # 发送POST请求获取成绩
            response = self.session.post(
                url, headers=headers, data=data, allow_redirects=False, timeout=10
            )
            if debug:
                logger.debug(f"响应状态码: {response.status_code}")
            if response.status_code != 200:
                raise Exception(f"请求失败，状态码: {response.status_code}")
            # 使用正则表达式解析JSON数据（模仿Dart代码的方式）
            html_content = response.text
            transcript_json_match = re.search(
                r'(?<="items":)\[(.*?)\](?=,"limit")', html_content
            )
            if not transcript_json_match:
                raise Exception("无法解析成绩数据")
            transcript_json = transcript_json_match.group(0)
            if debug:
                logger.debug(f"提取到的JSON数据: {transcript_json[:200]}...")
            # 解析JSON数据
            grades_data = json.loads(transcript_json)
            # 过滤有效的成绩记录（有xkkh课程号的）
            valid_grades = [grade for grade in grades_data if grade.get("xkkh")]
            logger.info(f"成功获取 {len(valid_grades)} 条成绩记录")
            return valid_grades
        except Exception as e:
            logger.error(f"获取成绩失败: {str(e)}")
            if debug:
                logger.debug(f"异常详情: {type(e).__name__}: {e}", exc_info=True)
            raise

    def logout(self):
        """登出"""
        self.jsessionid = None
        self.route = None
        self.logged_in = False
        self.session.cookies.clear()
        logger.info("已登出")


def fetch_grades_with_credentials(
    username, password, xn="", xq="", zscjl="", zscjr="", debug=True
):
    """
    使用用户名密码获取成绩
    参数:
        username - 学号
        password - 密码
        xn: 学年，默认 ""
        xq: 学期，默认 ""
        zscjl: 成绩段最小值，默认 ""
        zscjr: 成绩段最大值，默认 ""
        debug: 是否开启调试模式
    """
    client = ZdbkClient()
    try:
        # 登录
        if not client.login_with_credentials(username, password, debug):
            return None
        # 获取成绩
        grades = client.get_transcript(
            xn=xn, xq=xq, zscjl=zscjl, zscjr=zscjr, debug=debug
        )
        return grades
    except Exception as e:
        logger.error(f"获取成绩过程中出错: {str(e)}")
        return None
    finally:
        client.logout()


def fetch_grades_with_login(
    iplanet_directory_pro, xn="2024-2025", xq="2", zscjl="", zscjr="", debug=True
):
    """
    使用登录方式获取成绩
    参数:
        iplanet_directory_pro - iPlanetDirectoryPro cookie值
        xn: 学年，默认 "2024-2025"
        xq: 学期，默认 "2"
        zscjl: 综素成绩类型，默认 ""
        zscjr: 综素成绩人，默认 ""
        debug: 是否开启调试模式
    """
    client = ZdbkClient()
    try:
        # 登录
        if not client.login(iplanet_directory_pro, debug):
            return None
        # 获取成绩
        grades = client.get_transcript(
            xn=xn, xq=xq, zscjl=zscjl, zscjr=zscjr, debug=debug
        )
        return grades
    except Exception as e:
        logger.error(f"获取成绩过程中出错: {str(e)}")
        return None
    finally:
        client.logout()


def save_grades_to_file(grades, filename="grades.json", debug=True):
    """保存成绩到文件"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(grades, f, ensure_ascii=False, indent=2)
        logger.info(f"成功保存 {len(grades)} 条成绩到 {filename}")
        if debug:
            # 保存一个格式化的摘要文件
            summary_filename = filename.replace(".json", "_summary.txt")
            with open(summary_filename, "w", encoding="utf-8") as f:
                f.write(f"成绩摘要 - 共 {len(grades)} 门课程\n")
                f.write("=" * 50 + "\n\n")
                for i, grade in enumerate(grades, 1):
                    f.write(f"{i}. {grade.get('kcmc', '未知课程')}\n")
                    f.write(f"   成绩: {grade.get('cj', 'N/A')}\n")
                    f.write(f"   绩点: {grade.get('jd', 'N/A')}\n")
                    f.write(f"   学分: {grade.get('xf', 'N/A')}\n")
                    f.write(f"   课程号: {grade.get('xkkh', 'N/A')}\n\n")
            logger.info(f"成绩摘要保存到 {summary_filename}")
    except Exception as e:
        logger.error(f"保存文件失败: {e}")


if __name__ == "__main__":
    logger.info("程序开始执行")
    # 使用用户名密码直接登录
    USERNAME = "USERNAME_EXAMPLE"  # 学号
    PASSWORD = "PASSWORD_EXAMPLE"  # 密码
    # 查询参数
    QUERY_PARAMS = {
        "xn": "",  # 学年
        "xq": "",  # 学期 (1-秋冬学期, 2-春夏学期)
        "zscjl": "",  # 成绩段最小值
        "zscjr": "",  # 成绩段最大值
    }
    # 使用用户名密码获取成绩
    grades = fetch_grades_with_credentials(
        USERNAME,
        PASSWORD,
        xn=QUERY_PARAMS["xn"],
        xq=QUERY_PARAMS["xq"],
        zscjl=QUERY_PARAMS["zscjl"],
        zscjr=QUERY_PARAMS["zscjr"],
        debug=True,
    )
    # 保存结果到文件
    if grades:
        save_grades_to_file(grades, filename="grades_with_credentials.json", debug=True)
    else:
        logger.warning("未获取到成绩数据")

    logger.info("程序执行完成")
