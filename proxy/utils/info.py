import struct
from proxy.db import DATABASE

from loguru import logger

BACKPACK_TYPE_DICT = {0x00: "裝備", 0x01: "消費", 0x02: "其他", 0x03: "活動", 0x04: "寵物", 0x09: "倉庫[一般]", 0x0F: "倉庫[時尚]"}

CHANNEL_TYPE_DICT = {0x01: "一般", 0x05: "悄悄话"}


def get_content_info(data: bytes):
    if len(data) < 8:
        # 空包不解析
        return

    packet_length, packet_type, command, flag = struct.unpack("<HHHH", data[:8])
    content = data[8:]

    if packet_length == 12 and packet_type == 0x01 and command == 0x00:
        # 心跳包 0C 00 01 00 00 00 00 00 0C C3 E6 43
        logger.info(f"心跳: {content.hex(' ').upper()}")
        return

    match command:
        case 0xA469:
            # 技能初始化 14 00 01 00 69 A4 EB 0B 00 00 00 00 00 FF FF FF FF 00 00 00
            logger.info("動作->技能初始化成功")
        case 0xB536:
            # 超越技能初始化 08 00 01 00 36 B5 EB 0B
            logger.info("動作->超越技能初始化成功")
        case 0xA8FB:
            # 物品丢弃 0F 00 01 00 FB A8 EB 0B 01 00 00 00 03 01 00
            backpack_type, item_index, item_count = struct.unpack("<LBH", content)
            logger.info(f"動作->丟棄道具: 背包類型={BACKPACK_TYPE_DICT[backpack_type]}, 道具序號={item_index}, 道具數量={item_count}")
        case 0xA463:
            # 技能學習 18 00 01 00 63 A4 EB 0B 96 84 1B 00 00 00 00 00 00 FF FF FF FF 00 00 00
            skill_id = struct.unpack("<L", data[8:12])[0]
            logger.info(f"動作->技能學習: 技能ID={skill_id}, 技能名稱={DATABASE.get_skill_name_by_id(skill_id)}")
        case 0xA47F:
            # 技能加點 0F 00 01 00 7F A4 EB 0B 36 33 7A 00 00 08 00
            skill_id, _, skill_point = struct.unpack("<LBH", content)
            logger.info(f"動作->技能加點: 技能ID={skill_id}, 技能名稱={DATABASE.get_skill_name_by_id(skill_id)}, 技能點數={skill_point}")
        case 0xAE85:
            # 動作執行 14 00 01 00 85 AE EB 0B 04 00 00 00 00 00 00 00 00 00 00 00
            action_id, unknown = struct.unpack("<QL", content)
            logger.info(f"動作->動作執行: 動作ID={action_id}, 動作名稱={DATABASE.get_action_name_by_id(action_id)}, 其他參數={hex(unknown).upper()}")
        case 0xA47B:
            # 技能释放 15 00 01 00 7B A4 EB 0B 7C DC 10 00 00 01 00 02 FF FF FF FF 01
            skill_id, _, skill_type, order, _, awaken_order = struct.unpack("<LBHBLB", content)
            logger.info(f"動作->技能釋放: 技能ID={skill_id}, 技能名稱={DATABASE.get_skill_name_by_id(skill_id)}, 技能类型={skill_type}, 技能顺序={order}, 超越技能顺序={awaken_order}")
        case 0xAB3D:
            # 倉庫存錢 10 00 01 00 3D AB EB 0B A0 86 01 00 00 00 00 00
            ely = struct.unpack("<Q", content)[0]
            logger.info(f"動作->倉庫存款: 金額={ely}")
        case 0xAB3F:
            # 倉庫取錢 10 00 01 00 3F AB EB 0B A0 86 01 00 00 00 00 00
            ely = struct.unpack("<Q", content)[0]
            logger.info(f"動作->倉庫提款: 金額={ely}")
        case 0xA8F9 | 0xA8E8:
            # 轉移道具|拆分道具 14 00 01 00 F9 A8 EB 0B 01 00 00 00 02 01 00 09 00 00 00 05
            from_backpack_type, from_item_index, item_count, to_backpack_type, to_item_index = struct.unpack("<LBHLB", content)
            logger.info(f"動作->轉移道具: 原背包={BACKPACK_TYPE_DICT[from_backpack_type]}, 原道具位置={from_item_index}, 目的背包={BACKPACK_TYPE_DICT[to_backpack_type]}, 目的道具位置={to_item_index}, 道具數量={item_count}")
        case 0xA8FC:
            # 使用道具 15 00 01 00 FC A8 EB 0B 6F CC 00 00 01 00 10 30 01 00 00 00 1B
            backpack_type, item_index = struct.unpack("<LB", content[-5:])
            logger.info(f"動作->使用道具: 背包類型={BACKPACK_TYPE_DICT[backpack_type]}, 道具序號={item_index}")
        case 0xABC1:
            # 聊天 2D 00 01 00 C1 AB EB 0B 01 00 00 00 00 00 00 00 1C 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 31 00
            channel_id, message_length = struct.unpack("<QB", content[:9])
            message_content = content[-message_length:].decode("big5").strip()
            logger.info(f"動作->聊天: 频道ID={channel_id}, 频道名称={CHANNEL_TYPE_DICT.get(channel_id, '未知频道')}, 喊话内容={message_content}")
        case _:
            pass
            # logger.debug(f"{packet_length=}, {packet_type=}, {command=:04X}, {flag=:04X}, {content.hex(' ').upper()}")
