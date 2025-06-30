#!/usr/bin/env python3
"""
測試 CMoney API 的所有 table ID
"""

import requests
import json
import time
from typing import Dict, List
import logging

# 設定 logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# API 基礎 URL
BASE_URL = "https://www.cmoney.tw/MobileService/ashx/GetDtnoData.ashx"

# 測試用的股票代號
TEST_STOCK_ID = "2330"  # 台積電

# 所有要測試的 table ID
TABLE_IDS = [
    735975, 736028, 778132, 778134, 101779692, 101779729, 101780120, 101780121,
    101300620, 101780872, 101781221, 101781557, 101782076, 101782077, 101782447,
    101782826, 101782971, 101783172, 101856232, 101856252, 101780789, 101783819,
    101784079, 101572452, 101784744, 101784769, 94542884, 101785000, 789798,
    789801, 101963945, 101963955, 101855276, 101855290, 101856892, 101857332,
    101857333, 101857334, 101857360, 101899316, 101899317, 101899318, 919613,
    917347, 917345, 917466, 919618, 919626, 919629, 919604, 917346, 917344,
    917465, 919617, 919625, 919627, 935143, 935146, 935150, 935159, 935161,
    935162, 2551184, 2551192, 2551209, 309625, 935145, 935147, 935157, 935163,
    935165, 853230, 1992854, 2362712, 1236003, 101908165, 97316645, 2108782,
    7442501, 7627976, 99284118, 101909774, 917365, 917379, 917492, 917494,
    917497, 917717, 917662, 917664, 935255, 935257, 7627277, 7627174, 101911761,
    101911764, 917370, 917386, 917708, 974361, 917661, 917663, 935256, 935260,
    1557150, 101912970, 101914214, 4055459, 7616787, 7627867, 7628386, 7628415,
    97917861, 101915004, 789586, 782626, 101608103, 101608106, 101608132,
    101608133, 101609532, 101609556, 101610636, 101610637, 101610638, 1624711,
    101963146, 101963171, 101963501, 101963502, 2248208, 101947679, 101950154,
    101951436, 101951485, 1590233, 1556129, 102233267, 1624415, 1320825,
    101953829, 101953842, 3239174, 101966032, 101966321, 2037976, 2700571,
    101954428, 2037981, 5276635, 2037986, 2037989, 917503, 917505, 917506,
    101914544, 101914264, 101916662, 1557017, 2289778, 3239089, 3239091,
    917501, 917504, 102167882, 3239097, 3239286, 3239105, 3239106, 3239112,
    3239115, 3239165, 3239498, 1496126, 2592291, 101971485, 4638087, 4638130,
    4638149, 4638234, 4638194, 4639245, 4639309, 4639332, 4639360, 4639380,
    102004508, 102004538, 102004563, 102004605, 102004619, 102004633, 102004671,
    102005560, 102005561, 102005562, 102005575, 102005576, 102005577, 102005594,
    3239099, 3239100, 3239101, 3239103, 102006232, 102006588, 5781903, 5781927,
    102008269, 917490, 917486, 917362, 917364, 917373, 917377, 917369, 917371,
    917374, 917474, 102016661, 917472, 917473, 917475, 917759, 927748, 917761,
    917763, 917764, 917765, 919429, 919557, 917368, 917367, 917435, 917434,
    917791, 935218, 927791, 917439, 917792, 917794, 917800, 917793, 917802,
    917801, 917804, 917803, 917808, 917797, 917798, 935227, 917440, 917441,
    917442, 917445, 917444, 917449, 681599, 1992948, 1571254, 2106654, 917677,
    917678, 917679, 917680, 935172, 935173, 917387, 917388, 917389, 917390,
    917514, 917524, 917515, 917517, 917519, 917521, 917518, 917525, 917655,
    935244, 935246, 102132375, 102132580, 917523, 917357, 917533, 917671,
    917480, 935238, 917690, 917477, 935278, 102168437, 917816, 917818, 917458,
    917375, 917815, 917814, 917456, 4051301, 12799985, 12801414, 12818379,
    12819078, 12819545, 12822871, 13685890, 13685899, 13685908, 13685923,
    102172286, 102172595, 57188890, 102172940, 102173161, 4276910, 102228369,
    102228337, 24311489, 25949908, 25950322, 25898813
]

class CMoneyAPITester:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": "https://www.cmoney.tw/",
            "Accept": "application/json",
        }
        self.results = {}
    
    def test_table_id(self, table_id: int, stock_id: str = "2330") -> Dict:
        """
        測試單一 table ID
        
        Args:
            table_id: 要測試的 table ID
            stock_id: 測試用的股票代號
        
        Returns:
            Dict: 測試結果
        """
        try:
            # 建立 API URL
            url = f"{BASE_URL}?action=getdtnodata&DtNo={table_id}&ParamStr=AssignID={stock_id};MTPeriod=0;DTMode=0;DTRange=5;DTOrder=1;MajorTable=M173;&AssignSPID=&KeyMap=&FilterNo=0"
            
            logger.info(f"測試 Table ID: {table_id}")
            
            # 發送請求
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # 分析回應內容
                    result = {
                        "status": "success",
                        "status_code": response.status_code,
                        "has_data": bool(data.get("Data")),
                        "data_count": len(data.get("Data", [])),
                        "title": data.get("Title", []),
                        "url": url,
                        "response_size": len(response.text)
                    }
                    
                    # 如果有資料，記錄前幾筆作為範例
                    if data.get("Data"):
                        result["sample_data"] = data["Data"][:3]  # 前3筆資料
                    
                    logger.info(f"✅ Table ID {table_id}: 成功 (資料: {result['data_count']} 筆)")
                    
                except json.JSONDecodeError:
                    result = {
                        "status": "error",
                        "status_code": response.status_code,
                        "error": "JSON 解析失敗",
                        "response_text": response.text[:200],  # 前200字元
                        "url": url
                    }
                    logger.warning(f"⚠️  Table ID {table_id}: JSON 解析失敗")
                    
            else:
                result = {
                    "status": "error",
                    "status_code": response.status_code,
                    "error": f"HTTP {response.status_code}",
                    "url": url
                }
                logger.warning(f"❌ Table ID {table_id}: HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            result = {
                "status": "error",
                "error": "請求超時",
                "url": url
            }
            logger.error(f"⏰ Table ID {table_id}: 請求超時")
            
        except requests.exceptions.RequestException as e:
            result = {
                "status": "error",
                "error": f"請求錯誤: {str(e)}",
                "url": url
            }
            logger.error(f"❌ Table ID {table_id}: 請求錯誤 - {str(e)}")
            
        except Exception as e:
            result = {
                "status": "error",
                "error": f"未知錯誤: {str(e)}",
                "url": url
            }
            logger.error(f"💥 Table ID {table_id}: 未知錯誤 - {str(e)}")
        
        return result
    
    def test_all_tables(self, stock_id: str = "2330") -> Dict:
        """
        測試所有 table ID
        
        Args:
            stock_id: 測試用的股票代號
        
        Returns:
            Dict: 所有測試結果
        """
        logger.info(f"🚀 開始測試 {len(TABLE_IDS)} 個 Table ID...")
        logger.info(f"測試股票代號: {stock_id}")
        
        successful_count = 0
        error_count = 0
        
        for i, table_id in enumerate(TABLE_IDS, 1):
            logger.info(f"進度: {i}/{len(TABLE_IDS)}")
            
            result = self.test_table_id(table_id, stock_id)
            self.results[str(table_id)] = result
            
            if result["status"] == "success":
                successful_count += 1
            else:
                error_count += 1
            
            # 避免請求過於頻繁
            time.sleep(0.5)
        
        # 統計結果
        summary = {
            "total_tested": len(TABLE_IDS),
            "successful": successful_count,
            "error": error_count,
            "success_rate": f"{(successful_count/len(TABLE_IDS)*100):.1f}%"
        }
        
        logger.info(f"✅ 測試完成！成功: {successful_count}, 失敗: {error_count}, 成功率: {summary['success_rate']}")
        
        return {
            "summary": summary,
            "results": self.results
        }
    
    def save_results(self, filename: str = "cmoney_table_results.json"):
        """
        儲存測試結果到檔案
        
        Args:
            filename: 檔案名稱
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 結果已儲存到 {filename}")
    
    def get_successful_tables(self) -> List[int]:
        """
        取得成功的 table ID 列表
        
        Returns:
            List[int]: 成功的 table ID 列表
        """
        successful = []
        for table_id, result in self.results.items():
            if result["status"] == "success" and result["has_data"]:
                successful.append(int(table_id))
        return successful
    
    def print_summary(self):
        """
        印出測試摘要
        """
        successful = self.get_successful_tables()
        
        print("\n" + "="*60)
        print("📊 CMoney API 測試摘要")
        print("="*60)
        print(f"總測試數: {len(TABLE_IDS)}")
        print(f"成功數: {len(successful)}")
        print(f"失敗數: {len(TABLE_IDS) - len(successful)}")
        print(f"成功率: {(len(successful)/len(TABLE_IDS)*100):.1f}%")
        
        if successful:
            print(f"\n✅ 成功的 Table ID (前20個):")
            for i, table_id in enumerate(successful[:20], 1):
                result = self.results[str(table_id)]
                print(f"  {i:2d}. {table_id} - 資料: {result['data_count']} 筆")
            
            if len(successful) > 20:
                print(f"  ... 還有 {len(successful) - 20} 個成功的 Table ID")

def main():
    """主函數"""
    tester = CMoneyAPITester()
    
    try:
        # 測試所有 table ID
        all_results = tester.test_all_tables()
        
        # 儲存結果
        tester.save_results()
        
        # 印出摘要
        tester.print_summary()
        
        # 儲存成功的 table ID 列表
        successful_tables = tester.get_successful_tables()
        with open("successful_table_ids.json", 'w', encoding='utf-8') as f:
            json.dump(successful_tables, f, indent=2)
        
        logger.info(f"💾 成功的 Table ID 已儲存到 successful_table_ids.json")
        
    except KeyboardInterrupt:
        logger.info("⏹️  測試被使用者中斷")
    except Exception as e:
        logger.error(f"💥 測試過程中發生錯誤: {str(e)}")

if __name__ == "__main__":
    main() 