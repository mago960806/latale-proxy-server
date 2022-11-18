import struct
from proxy.db import DATABASE

from loguru import logger

BACKPACK_TYPE_DICT = {0x00: "裝備", 0x01: "消費", 0x02: "其他", 0x03: "活動", 0x04: "寵物", 0x09: "倉庫[一般]", 0x0F: "倉庫[時尚]"}

CHANNEL_TYPE_DICT = {0x01: "一般", 0x05: "悄悄话"}


def get_received_data(data: bytes):
    packet_length, packet_type, command = struct.unpack("<HHI", data[:8])
    content = data[8:]

    match command:
        case 200000700:
            # 怪物刷新 C1 00 01 00 BC C4 EB 0B 52 1D 00 00 23 A5 47 30 52 1D 00 00 23 A5 47 30 3F 3F 20 3F 3F 3F 3F 00 00 00 00 00 00 00 00 00 B9 00 86 05 00 00 86 05 00 00 A2 B3 96 00 00 00 00 00 A2 B3 96 00 00 00 00 00 A2 B3 96 00 00 00 00 00 97 03 03 00 00 00 00 00 86 05 00 00 2A 00 00 00 00 00 00 00 00 00 00 00 00 00 00 1C 43 00 00 48 C4 00 00 00 00 00 00 00 00 00 00 C8 44 00 00 F0 41 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 09 00 00 00 00 00 60 44 00 C0 7F 44 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
            pass
        case _:
            logger.debug(f"{packet_length=}, {packet_type=}, {command=}, content={content.hex(' ').upper()}")


def get_sent_data(data: bytes):
    packet_length, packet_type, command = struct.unpack("<HHI", data[:8])
    content = data[8:]

    match command:
        case 0:
            # 心跳包 0C 00 01 00 00 00 00 00 0C C3 E6 43
            timestamp = struct.unpack("<I", content)[0]
            logger.info(f"心跳: {timestamp}")
        case 200001816:
            # 技能初始化 14 00 01 00 69 A4 EB 0B 00 00 00 00 00 FF FF FF FF 00 00 00
            logger.info("動作->技能初始化成功")
        case 200005703:
            # 超越技能初始化 08 00 01 00 36 B5 EB 0B
            logger.info("動作->超越技能初始化成功")
        case 200000906:
            # 物品丢弃 0F 00 01 00 FB A8 EB 0B 01 00 00 00 03 01 00
            backpack_type, item_index, item_count = struct.unpack("<IBH", content)
            logger.info(f"動作->丟棄道具: 背包類型={BACKPACK_TYPE_DICT[backpack_type]}, 道具序號={item_index}, 道具數量={item_count}")
        case 200001810:
            # 技能學習 18 00 01 00 63 A4 EB 0B 96 84 1B 00 00 00 00 00 00 FF FF FF FF 00 00 00
            skill_id = struct.unpack("<I", data[8:12])[0]
            logger.info(f"動作->技能學習: 技能ID={skill_id}, 技能名稱={DATABASE.get_skill_name_by_id(skill_id)}")
        case 200001806:
            # 技能加點 0F 00 01 00 7F A4 EB 0B 36 33 7A 00 00 08 00
            skill_id, _, skill_point = struct.unpack("<IBH", content)
            logger.info(f"動作->技能加點: 技能ID={skill_id}, 技能名稱={DATABASE.get_skill_name_by_id(skill_id)}, 技能點數={skill_point}")
        case 200000500:
            # 動作執行 14 00 01 00 85 AE EB 0B 04 00 00 00 00 00 00 00 00 00 00 00
            action_id, unknown = struct.unpack("<QI", content)
            logger.info(f"動作->動作執行: 動作ID={action_id}, 動作名稱={DATABASE.get_action_name_by_id(action_id)}, 其他參數={hex(unknown).upper()}")
        case 200001802:
            # 技能释放 15 00 01 00 7B A4 EB 0B 7C DC 10 00 00 01 00 02 FF FF FF FF 01
            skill_id, _, skill_type, order, _, awaken_order = struct.unpack("<IBHBIB", content)
            logger.info(f"動作->技能釋放: 技能ID={skill_id}, 技能名稱={DATABASE.get_skill_name_by_id(skill_id)}, 技能类型={skill_type}, 技能顺序={order}, 超越技能顺序={awaken_order}")
        case 200001100:
            # 倉庫存錢 10 00 01 00 3D AB EB 0B A0 86 01 00 00 00 00 00
            ely = struct.unpack("<Q", content)[0]
            logger.info(f"動作->倉庫存款: 金額={ely}")
        case 200001102:
            # 倉庫取錢 10 00 01 00 3F AB EB 0B A0 86 01 00 00 00 00 00
            ely = struct.unpack("<Q", content)[0]
            logger.info(f"動作->倉庫提款: 金額={ely}")
        case 200000904 | 200000921:
            # 轉移道具|拆分道具 14 00 01 00 F9 A8 EB 0B 01 00 00 00 02 01 00 09 00 00 00 05
            from_backpack_type, from_item_index, item_count, to_backpack_type, to_item_index = struct.unpack("<IBHIB", content)
            logger.info(f"動作->轉移道具: 原背包={BACKPACK_TYPE_DICT[from_backpack_type]}, 原道具位置={from_item_index}, 目的背包={BACKPACK_TYPE_DICT[to_backpack_type]}, 目的道具位置={to_item_index}, 道具數量={item_count}")
        case 200000909:
            # 使用道具 15 00 01 00 FC A8 EB 0B 6F CC 00 00 01 00 10 30 01 00 00 00 1B
            backpack_type, item_index = struct.unpack("<IB", content[-5:])
            logger.info(f"動作->使用道具: 背包類型={BACKPACK_TYPE_DICT[backpack_type]}, 道具序號={item_index}")
        case 200000902:
            # 道具拾取 1A 00 01 00 86 C5 EB 0B 4A 9D 00 00 80 A7 84 30 00 8F E3 CD 04 00 00 00 00 01
            #         1A 00 01 00 86 C5 EB 0B EB A1 00 00 80 A7 84 30 00 D1 B6 28 0A 01 00 00 00 0F
            bag_index, bag_id, item_index, item_id, backpack_type, backpack_index = struct.unpack("<LLBLLB", content)
            logger.info(f"動作->道具拾取: 包裹序號={bag_index}, 包裹ID={bag_id}, 道具序號={item_index}, 道具ID={item_id}, 背包類型={BACKPACK_TYPE_DICT[backpack_type]}, 背包序號={backpack_index}")
        case 200001200:
            # 聊天 2D 00 01 00 C1 AB EB 0B 01 00 00 00 00 00 00 00 1C 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 00
            channel_id, message_length = struct.unpack("<QB", content[:9])
            message_content = content[-message_length:].decode("big5").strip()
            logger.info(f"動作->聊天: 频道ID={channel_id}, 频道名称={CHANNEL_TYPE_DICT.get(channel_id, '未知频道')}, 喊话内容={message_content}")
        case 200004306:
            # 開始答題 0F 00 01 00 D2 D2 EB 0B FF FF FF FF 00 00 00
            logger.info(f"動作->開始答題")
        case 200004321:
            # 題目 12 00 01 00 E1 D2 EB 0B 0E 00 00 00 01 01 A0 3C CA 40
            quiz_number, answer, answer_type, _ = struct.unpack("<IBBI", content)
            logger.info(f"動作->提交答案: 題目序號={quiz_number}, 回答序號={answer}, 回答類型={answer_type}")
        case 200004326:
            # 題目 13 00 01 00 E6 D2 EB 0B 0F 00 00 00 FF FF FF FF 00 00 00
            quiz_number = struct.unpack("<IIHB", content)[0]
            logger.info(f"動作->提交答案: 题号={quiz_number}")
        case _:
            logger.debug(f"{packet_length=}, {packet_type=}, {command=}, content={content.hex(' ').upper()}")
