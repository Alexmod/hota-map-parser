# -*- coding: utf-8 -*-

import gzip
import json
import struct
import sys
from collections import Counter

TOWN_PORTAL_SPELL_ID = 9

PLAUSIBLE_MAP_SIZES = {36, 72, 108, 144, 180, 216, 252}

PLAYER_NAMES = {
    0: "Red",
    1: "Blue",
    2: "Tan",
    3: "Green",
    4: "Orange",
    5: "Purple",
    6: "Teal",
    7: "Pink",
    255: "Neutral",
}

SPELL_NAMES = {
    0: "Summon Boat",
    1: "Scuttle Boat",
    2: "Visions",
    3: "View Earth",
    4: "Disguise",
    5: "View Air",
    6: "Fly",
    7: "Water Walk",
    8: "Dimension Door",
    9: "Town Portal",
    10: "Quicksand",
    11: "Land Mine",
    12: "Force Field",
    13: "Fire Wall",
    14: "Earthquake",
    15: "Magic Arrow",
    16: "Ice Bolt",
    17: "Lightning Bolt",
    18: "Implosion",
    19: "Chain Lightning",
    20: "Frost Ring",
    21: "Fireball",
    22: "Inferno",
    23: "Meteor Shower",
    24: "Death Ripple",
    25: "Destroy Undead",
    26: "Armageddon",
    27: "Shield",
    28: "Air Shield",
    29: "Fire Shield",
    30: "Protection from Air",
    31: "Protection from Fire",
    32: "Protection from Water",
    33: "Protection from Earth",
    34: "Anti-Magic",
    35: "Dispel",
    36: "Magic Mirror",
    37: "Cure",
    38: "Resurrection",
    39: "Animate Dead",
    40: "Sacrifice",
    41: "Bless",
    42: "Curse",
    43: "Bloodlust",
    44: "Precision",
    45: "Weakness",
    46: "Stone Skin",
    47: "Disrupting Ray",
    48: "Prayer",
    49: "Mirth",
    50: "Sorrow",
    51: "Fortune",
    52: "Misfortune",
    53: "Haste",
    54: "Slow",
    55: "Slayer",
    56: "Frenzy",
    57: "Titan's Lightning Bolt",
    58: "Counterstrike",
    59: "Berserk",
    60: "Hypnotize",
    61: "Forgetfulness",
    62: "Blind",
    63: "Teleport",
    64: "Remove Obstacle",
    65: "Clone",
    66: "Fire Elemental",
    67: "Earth Elemental",
    68: "Water Elemental",
    69: "Air Elemental",
}

ARTIFACT_NAMES = {
    8: "Blackshard of the Dead Knight",
    26: "Rib Cage",
    60: "Bow of Elven Cherrywood",
    61: "Bowstring of the Unicorn's Mane",
    62: "Angel Feather Arrows",
    86: "Tome of Fire Magic",
    87: "Tome of Air Magic",
    88: "Tome of Water Magic",
    89: "Tome of Earth Magic",
    91: "Golden Bow",
    115: "Endless Sack of Gold",
    116: "Endless Bag of Gold",
    117: "Endless Purse of Gold",
    128: "Armageddon's Blade",
    137: "Bow of the Sharpshooter",
}

ARTIFACT_ALIASES = {
    "blackshard": 8,
    "blackshard of the dead knight": 8,
    "меч мертвого рыцаря": 8,
    "меч мёртвого рыцаря": 8,
    "rib": 26,
    "rib cage": 26,
    "ribs": 26,
    "ребра": 26,
    "рёбра": 26,
    "bow of elven cherrywood": 60,
    "elven bow": 60,
    "golden bow": 91,
    "золотой лук": 91,
    "золотого лука": 91,
    "tome of fire magic": 86,
    "книга огня": 86,
    "tome of air magic": 87,
    "книга воздуха": 87,
    "tome of water magic": 88,
    "книга воды": 88,
    "tome of earth magic": 89,
    "книга земли": 89,
    "bow of the sharpshooter": 137,
    "лук снайпера": 137,
}

HERO_NAMES = {
    144: "Sir Mullich",
    145: "Adrienne",
    146: "Catherine",
    147: "Dracon",
    148: "Gelu",
    149: "Kilgor",
    150: "Lord Haart",
    151: "Mutare",
    152: "Roland",
    153: "Mutare Drake",
    154: "Boragus",
    155: "Xeron",
}

HERO_ALIASES = {
    "sir mullich": 144,
    "муллич": 144,
    "адриенна": 145,
    "adrienne": 145,
    "dracon": 147,
    "дракон": 147,
    "gelu": 148,
    "гелу": 148,
    "kilgor": 149,
    "килгор": 149,
    "lord haart": 150,
    "лорд хаарт": 150,
    "mutare": 151,
    "мутаре": 151,
    "roland": 152,
    "роланд": 152,
    "xeron": 155,
    "ксерон": 155,
}

TOWN_TYPES = {
    0: "Castle",
    1: "Rampart",
    2: "Tower",
    3: "Inferno",
    4: "Necropolis",
    5: "Dungeon",
    6: "Stronghold",
    7: "Fortress",
    8: "Conflux",
    9: "Cove",
}

OBJ_NAMES = {
    5: "Artifact",
    6: "Pandora's Box",
    26: "Event",
    34: "Hero",
    43: "One-way monolith entrance",
    44: "One-way monolith exit",
    45: "Two-way monolith",
    62: "Prison",
    70: "Random Hero",
    81: "Scholar",
    83: "Seer's Hut",
    93: "Spell Scroll",
    98: "Town",
}

OBJECT_KIND_BY_CLASS = {
    5: "artifact",
    6: "pandora",
    16: "bank",
    17: "owner32",
    20: "owner32",
    24: "bank",
    25: "bank",
    26: "event",
    33: "garrison",
    34: "hero",
    36: "grail",
    42: "owner32",
    53: "owner32",
    54: "monster",
    59: "sign",
    62: "hero",
    65: "artifact",
    66: "artifact",
    67: "artifact",
    68: "artifact",
    69: "artifact",
    70: "hero",
    71: "monster",
    72: "monster",
    73: "monster",
    74: "monster",
    75: "monster",
    76: "resource",
    77: "town",
    79: "resource",
    81: "scholar",
    83: "seer",
    84: "bank",
    85: "bank",
    87: "owner32",
    88: "shrine",
    89: "shrine",
    90: "shrine",
    91: "sign",
    93: "scroll",
    98: "town",
    113: "witch",
    162: "monster",
    163: "monster",
    164: "monster",
    214: "hero_placeholder",
    215: "quest_guard",
    216: "random_dwelling",
    217: "random_dwelling_level",
    218: "random_dwelling_faction",
    219: "garrison",
    220: "owner32",
}

OBJECT_KIND_BY_CLASS_AND_SUBTYPE = {
    (9, 1000): "quest_guard",
    (53, 7): "abandoned_mine",
    (220, 7): "abandoned_mine",
}

BUILDINGS = [
    ["TownHall", "CityHall", "Capitol", "Fort", "Citadel", "Castle", "Tavern", "Blacksmith"],
    ["Marketplace", "ResourceSilo", "ArtifactMerchants", "MageGuild1", "MageGuild2", "MageGuild3", "MageGuild4", "MageGuild5"],
    ["Shipyard", "Grail", "Special1", "Special2", "Special3", "Special4", "Dwelling1", "DwellingUp1"],
    ["Horde1", "Dwelling2", "DwellingUp2", "Horde2", "Dwelling3", "Dwelling4", "Horde3", "DwellingUp3"],
    ["DwellingUp4", "Horde4", "Dwelling5", "DwellingUp5", "Horde5", "Dwelling6", "DwellingUp6", "Dwelling7"],
    ["DwellingUp7", None, None, None, None, None, None, None],
]


class Reader:
    def __init__(self, data):
        self.data = data
        self.offset = 0

    def tell(self):
        return self.offset

    def _need(self, count):
        if self.offset + count > len(self.data):
            raise EOFError(f"need {count} bytes at {self.offset}, len={len(self.data)}")

    def bytes(self, count):
        self._need(count)
        value = self.data[self.offset : self.offset + count]
        self.offset += count
        return value

    def u8(self):
        self._need(1)
        value = self.data[self.offset]
        self.offset += 1
        return value

    def i8(self):
        value = self.u8()
        return value - 256 if value >= 128 else value

    def u16(self):
        self._need(2)
        value = struct.unpack_from("<H", self.data, self.offset)[0]
        self.offset += 2
        return value

    def i16(self):
        self._need(2)
        value = struct.unpack_from("<h", self.data, self.offset)[0]
        self.offset += 2
        return value

    def u32(self):
        self._need(4)
        value = struct.unpack_from("<I", self.data, self.offset)[0]
        self.offset += 4
        return value

    def i32(self):
        self._need(4)
        value = struct.unpack_from("<i", self.data, self.offset)[0]
        self.offset += 4
        return value

    def bool(self):
        return self.u8() != 0

    def string(self):
        length = self.u32()
        return self.bytes(length).decode("cp1251", "replace")

    def coord(self):
        return (self.u8(), self.u8(), self.u8())

    def skip(self, count):
        self.bytes(count)


def bitmask(reader, byte_count, item_count, invert=False):
    """Читает битовую маску и возвращает номера включенных элементов."""
    result = set()
    raw = []
    for byte_index in range(byte_count):
        mask = reader.u8()
        raw.append(mask)
        for bit in range(8):
            index = byte_index * 8 + bit
            if index < item_count and (bool(mask & (1 << bit)) != invert):
                result.add(index)
    return result, raw


def read_artifact(reader):
    value = reader.u16()
    return None if value == 0xFFFF else value


def read_artifact32(reader):
    value = reader.u32()
    return None if value == 0xFFFFFFFF else value


def read_creature(reader):
    value = reader.u16()
    return None if value == 0xFFFF else value


def read_hero(reader):
    value = reader.u8()
    return None if value == 0xFF else value


def read_player(reader):
    value = reader.u8()
    return 255 if value == 255 else value


def read_player32(reader):
    value = reader.u32()
    return 255 if value == 255 else value


def read_spell8(reader):
    value = reader.u8()
    return None if value == 0xFF else value


def read_spell32(reader):
    value = reader.i32()
    return None if value in (-1, 0xFFFFFFFF) else value


def read_resources(reader):
    return [reader.i32() for _ in range(7)]


def read_primary(reader):
    return [reader.u8() for _ in range(4)]


def read_secondary(reader):
    return (reader.u8(), reader.u8())


def read_creatures(reader):
    return [(read_creature(reader), reader.u16()) for _ in range(7)]


def read_message_and_guards(reader):
    """Читает необязательное сообщение объекта и охрану, если они есть."""
    if not reader.bool():
        return None
    message = reader.string()
    creatures = []
    if reader.bool():
        creatures = read_creatures(reader)
    reader.skip(4)
    return {"message": message, "creatures": creatures}


def read_hero_artifacts_if_present(reader, wide_artifacts=False):
    if not reader.bool():
        return None
    artifact_reader = read_artifact32 if wide_artifacts else read_artifact
    equipped = [artifact_reader(reader) for _ in range(19)]
    backpack = [artifact_reader(reader) for _ in range(reader.u16())]
    return {"equipped": equipped, "backpack": backpack}


def read_event_base(reader, wide_artifacts=False):
    """Читает общую награду события или ящика Пандоры."""
    event = {
        "guardians": read_message_and_guards(reader),
        "experience": reader.i32(),
        "spell_points": reader.i32(),
        "morale": reader.i8(),
        "luck": reader.i8(),
        "resources": read_resources(reader),
        "primary": read_primary(reader),
    }
    artifact_reader = read_artifact32 if wide_artifacts else read_artifact
    event["secondary"] = [read_secondary(reader) for _ in range(reader.u8())]
    event["artifacts"] = [artifact_reader(reader) for _ in range(reader.u8())]
    event["spells"] = [read_spell8(reader) for _ in range(reader.u8())]
    event["creatures"] = [(read_creature(reader), reader.u16()) for _ in range(reader.u8())]
    reader.skip(8)
    return event


def read_reward_resource_or_primary(reader):
    return reader.u32()


def read_reward_primary_delta(reader):
    return reader.i8()


def read_reward_secondary_skill(reader):
    return (reader.u8(), reader.u32())


def read_reward_artifact_with_count(reader):
    return (reader.u8(), reader.u8())


def read_reward_creature(reader):
    return (read_creature(reader), reader.u16())


REWARD_READERS = {
    0: lambda reader: None,
    1: read_reward_resource_or_primary,
    2: read_reward_resource_or_primary,
    3: read_reward_primary_delta,
    4: read_reward_primary_delta,
    5: read_reward_secondary_skill,
    6: read_reward_artifact_with_count,
    7: read_secondary,
    8: read_artifact,
    9: read_spell8,
    10: read_reward_creature,
}


def read_reward(reader):
    """Читает награду Seer's Hut в зависимости от ее типа."""
    reward_type = reader.u8()
    try:
        value = REWARD_READERS[reward_type](reader)
    except KeyError as exc:
        raise ValueError(f"bad reward type {reward_type} at {reader.tell() - 1}") from exc
    return {"type": reward_type, "value": value}


def read_quest_artifacts(reader):
    return [read_artifact(reader) for _ in range(reader.u8())]


def read_quest_creatures(reader):
    return [(read_creature(reader), reader.u16()) for _ in range(reader.u8())]


def read_hota_multi_hero_classes(reader, details):
    count = reader.u32()
    details["hero_classes"], _ = bitmask(reader, (count + 7) // 8, count)


def read_hota_multi_value(reader, details):
    details["value"] = reader.u32()


def read_hota_multi_script(reader, details):
    details["script_id"] = reader.u32()
    details["unknown"] = reader.bool()


HOTA_MULTI_QUEST_READERS = {
    0: read_hota_multi_hero_classes,
    1: read_hota_multi_value,
    2: read_hota_multi_value,
    3: read_hota_multi_script,
}


def read_hota_multi_quest(reader):
    subtype = reader.u32()
    details = {"hota_multi_subtype": subtype}
    handler = HOTA_MULTI_QUEST_READERS.get(subtype)
    if handler:
        handler(reader, details)
    return details


QUEST_DETAIL_READERS = {
    0: lambda reader: None,
    1: lambda reader: reader.u32(),
    2: read_primary,
    3: lambda reader: reader.u32(),
    4: lambda reader: reader.u32(),
    5: read_quest_artifacts,
    6: read_quest_creatures,
    7: read_resources,
    8: read_hero,
    9: read_player,
    10: read_hota_multi_quest,
}


def read_quest(reader):
    """Читает условие квеста и связанные с ним тексты."""
    quest_type = reader.u8()
    try:
        details = QUEST_DETAIL_READERS[quest_type](reader)
    except KeyError as exc:
        raise ValueError(f"bad quest type {quest_type} at {reader.tell() - 1}") from exc

    quest = {"type": quest_type, "details": details}
    if quest_type != 0:
        quest["deadline"] = reader.i32()
        quest["proposal"] = reader.string()
        quest["progress"] = reader.string()
        quest["completion"] = reader.string()
    return quest


def read_timed_event(reader, hota_v3=False):
    """Читает глобальное или городское событие с учетом версии HotA."""
    event = {
        "name": reader.string(),
        "message": reader.string(),
        "resources": read_resources(reader),
    }
    event["players"], _ = bitmask(reader, 1, 8)
    event["human"] = reader.bool()
    event["computer"] = reader.bool()
    event["first"] = reader.u16()
    if hota_v3:
        event["repeat"] = reader.u8()
        reader.skip(17)
    else:
        event["repeat"] = reader.u16()
        reader.skip(16)
    return event


def read_town_event(reader, building_bytes=6, hota_v3=False):
    """Читает событие города, включая здания и прирост существ."""
    event = read_timed_event(reader, hota_v3)
    event["buildings_raw"] = list(reader.bytes(building_bytes))
    event["creatures"] = [reader.u16() for _ in range(7)]
    reader.skip(4)
    return event


def decode_buildings(raw):
    """Преобразует битовую маску построек города в набор имен зданий."""
    result = set()
    for byte_index, mask in enumerate(raw):
        for bit in range(8):
            if mask & (1 << bit):
                name = BUILDINGS[byte_index][bit] if byte_index < len(BUILDINGS) else f"B{byte_index * 8 + bit}"
                if name:
                    result.add(name)
    return result


def active_tiles(position, active_raw):
    """Восстанавливает клетки карты, на которых объект считается активным."""
    x, y, z = position
    result = []
    for row, mask in enumerate(active_raw):
        for bit in range(8):
            if mask & (1 << bit):
                result.append((x - 7 + bit, y - 5 + row, z))
    return result


def is_hota_v3(info):
    """Проверяет, что карта использует расширенный формат объектов HotA."""
    return info.get("format") == 32 and info.get("hota_format1", 0) >= 3


def town_building_bytes(info):
    """Возвращает размер битовых масок зданий для версии HotA этой карты."""
    return 7 if info.get("hota_format1", 0) >= 9 else 6


def find_basic_info_offset(data, start):
    """Ищет начало базового заголовка, когда перед ним есть HotA-поля неизвестной длины."""
    candidates = []
    limit = min(start + 128, len(data) - 12)
    for offset in range(start, limit):
        if data[offset] not in (0, 1):
            continue

        size = struct.unpack_from("<I", data, offset + 1)[0]
        has_two_levels = data[offset + 5]
        name_len = struct.unpack_from("<I", data, offset + 6)[0]
        if size not in PLAUSIBLE_MAP_SIZES or has_two_levels not in (0, 1) or not 0 <= name_len <= 64:
            continue

        name_start = offset + 10
        name_end = name_start + name_len
        if name_end + 6 > len(data):
            continue

        name_raw = data[name_start:name_end]
        if b"\x00" in name_raw:
            continue

        desc_len = struct.unpack_from("<I", data, name_end)[0]
        desc_end = name_end + 4 + desc_len
        if not 0 <= desc_len <= 200000 or desc_end + 2 > len(data):
            continue

        difficulty = data[desc_end]
        if difficulty <= 4:
            candidates.append(offset)

    if not candidates:
        raise ValueError("could not locate HotA basic-info header")
    return candidates[0]


def read_minimal_header(data):
    """Читает только ту часть заголовка, которая нужна для поиска карты и объектов."""
    reader = Reader(data)
    info = {"format": reader.u32()}
    if info["format"] != 32:
        raise ValueError(f"expected HotA format 32, got {info['format']}")

    info["hota_format1"] = reader.u32()
    basic_offset = find_basic_info_offset(data, reader.tell())
    extra = data[reader.tell() : basic_offset]
    info["hota_format2"] = struct.unpack_from("<H", extra, 0)[0] if len(extra) >= 2 else None
    info["hota_header_extra"] = list(extra)
    info["basic_info_offset"] = basic_offset

    reader.offset = basic_offset
    info["is_playable"] = reader.bool()
    info["size"] = reader.u32()
    info["levels"] = 2 if reader.bool() else 1
    info["name"] = reader.string()
    info["description"] = reader.string()
    info["difficulty"] = reader.u8()
    info["max_level"] = reader.u8()
    return info, reader


def read_templates(reader, expected_count=None):
    """Читает таблицу шаблонов объектов: def, class, subtype и маски клеток."""
    count = reader.u32() if expected_count is None else expected_count
    templates = []
    for index in range(count):
        template = {
            "index": index,
            "def": reader.string(),
            "pass_raw": list(reader.bytes(6)),
            "active_raw": list(reader.bytes(6)),
            "allowed_landscapes": reader.u16(),
            "landscape_group": reader.u16(),
            "class": reader.u32(),
            "subtype": reader.u32(),
            "group": reader.u8(),
            "above": reader.u8(),
        }
        reader.skip(16)
        templates.append(template)
    return templates


def find_template_offset(data, size, levels):
    """Находит таблицу шаблонов по строкам .def, если полный заголовок не разобран."""
    lower = data.lower()
    search_from = max(0, size * size * levels * 7 // 2)
    pos = lower.find(b".def", search_from)
    while pos != -1:
        for string_start in range(max(0, pos - 80), pos + 1):
            if string_start < 8:
                continue

            length = struct.unpack_from("<I", data, string_start - 4)[0]
            if length != pos + 4 - string_start:
                continue

            count_offset = string_start - 8
            count = struct.unpack_from("<I", data, count_offset)[0]
            if not 0 < count < 10000:
                continue

            try:
                probe = Reader(data)
                probe.offset = count_offset
                templates = read_templates(probe)
                object_count = probe.u32()
                if 0 <= object_count < 250000:
                    return count_offset, templates, object_count, probe.tell()
            except Exception:
                pass

        pos = lower.find(b".def", pos + 4)

    raise ValueError("could not locate object template table")


def property_type(object_class, subtype):
    """Переводит class/subtype из H3M в имя обработчика данных объекта."""
    return OBJECT_KIND_BY_CLASS_AND_SUBTYPE.get(
        (object_class, subtype),
        OBJECT_KIND_BY_CLASS.get(object_class, "none"),
    )


def read_artifact_object(reader, obj):
    """Дочитывает данные артефакта на карте: сообщение и охрану."""
    obj["guardians"] = read_message_and_guards(reader)


def read_bank_object(reader, obj, info):
    """Дочитывает данные банка существ в новых HotA-форматах."""
    if is_hota_v3(info):
        obj["content"] = reader.u32()
        upgraded = reader.u8()
        obj["upgraded"] = None if upgraded == 0xFF else bool(upgraded)
        obj["artifacts"] = [read_artifact32(reader) for _ in range(reader.u32())]


def read_event_object(reader, obj, info):
    """Дочитывает объект-событие на карте и его ограничения по игрокам."""
    obj["event"] = read_event_base(reader, is_hota_v3(info))
    obj["players"], _ = bitmask(reader, 1, 8)
    obj["computer"] = reader.bool()
    obj["remove"] = reader.bool()
    reader.skip(4)
    if is_hota_v3(info):
        obj["human"] = reader.bool()


def read_garrison_object(reader, obj):
    """Дочитывает гарнизон: владельца, войска и флаг удаления."""
    obj["owner"] = read_player32(reader)
    obj["creatures"] = read_creatures(reader)
    obj["removable"] = reader.bool()
    reader.skip(8)


def read_grail_object(reader, obj):
    """Дочитывает область подсказки Грааля."""
    obj["radius"] = reader.u32()


def read_hero_object(reader, obj, info):
    """Дочитывает героя или тюрьму с его настройками и армией."""
    obj["object_id"] = reader.u32()
    obj["owner"] = read_player(reader)
    obj["hero"] = read_hero(reader)
    if reader.bool():
        obj["name"] = reader.string()
    if reader.bool():
        obj["experience"] = reader.u32()
    if reader.bool():
        obj["portrait"] = read_hero(reader)
    if reader.bool():
        obj["skills"] = [read_secondary(reader) for _ in range(reader.u32())]
    if reader.bool():
        obj["creatures"] = read_creatures(reader)
    obj["formation"] = reader.u8()
    obj["artifacts"] = read_hero_artifacts_if_present(reader, is_hota_v3(info))
    obj["patrol"] = reader.u8()
    if reader.bool():
        obj["biography"] = reader.string()
    obj["gender"] = reader.i8()
    if reader.bool():
        obj["spells"], _ = bitmask(reader, 9, 70)
    if reader.bool():
        obj["primary"] = read_primary(reader)
    reader.skip(16)


def read_monster_object(reader, obj, info):
    """Дочитывает нейтральный отряд и возможную награду за бой."""
    obj["object_id"] = reader.u32()
    obj["count"] = reader.u16()
    obj["disposition"] = reader.u8()
    if reader.bool():
        obj["message"] = reader.string()
        obj["resources"] = read_resources(reader)
        obj["artifact"] = read_artifact(reader)
    obj["never_flees"] = reader.bool()
    obj["no_grow"] = reader.bool()
    reader.skip(2)
    if is_hota_v3(info):
        exact = reader.u32()
        obj["exact_aggression"] = None if exact == 0xFFFFFFFF else exact
        obj["join_only_for_money"] = reader.bool()
        obj["join_percentage"] = reader.u32()
        upgraded = reader.u32()
        split = reader.u32()
        obj["upgraded_stack"] = None if upgraded == 0xFFFFFFFF else upgraded
        obj["split_stack"] = None if split == 0xFFFFFFFF else split


def read_pandora_object(reader, obj, info):
    """Дочитывает ящик Пандоры как событие с наградой."""
    obj["event"] = read_event_base(reader, is_hota_v3(info))


def read_hero_placeholder_object(reader, obj):
    """Дочитывает placeholder героя для сценарных настроек."""
    obj["owner"] = read_player(reader)
    obj["hero"] = read_hero(reader)
    if obj["hero"] is None:
        obj["power"] = reader.u8()


def read_quest_guard_object(reader, obj):
    """Дочитывает quest guard: условие прохода."""
    obj["quest"] = read_quest(reader)


def read_random_dwelling_object(reader, obj):
    """Дочитывает случайное жилище с диапазоном уровней существ."""
    obj["owner"] = read_player32(reader)
    obj["identifier"] = reader.u32()
    if obj["identifier"] == 0:
        obj["alignment"], _ = bitmask(reader, 2, 10)
    obj["min_level"] = reader.u8()
    obj["max_level"] = reader.u8()


def read_random_dwelling_level_object(reader, obj):
    """Дочитывает случайное жилище, где задан уровень существ."""
    obj["owner"] = read_player32(reader)
    obj["identifier"] = reader.u32()
    if obj["identifier"] == 0:
        obj["alignment"], _ = bitmask(reader, 2, 10)


def read_random_dwelling_faction_object(reader, obj):
    """Дочитывает случайное жилище, где задана фракция."""
    obj["owner"] = read_player32(reader)
    obj["min_level"] = reader.u8()
    obj["max_level"] = reader.u8()


def read_resource_object(reader, obj):
    """Дочитывает ресурс на карте: охрану и количество."""
    obj["guardians"] = read_message_and_guards(reader)
    obj["quantity"] = reader.u32()
    reader.skip(4)


def read_scholar_object(reader, obj):
    """Дочитывает ученого: тип награды и ее значение."""
    obj["reward_type"] = reader.i8()
    obj["reward"] = reader.u8()
    reader.skip(6)


def read_seer_object(reader, obj, info):
    """Дочитывает Seer's Hut и его награды, включая новые HotA-списки."""
    if is_hota_v3(info):
        obj["seer_quests"] = []
        for _ in range(reader.u32()):
            quest = read_quest(reader)
            reward = read_reward(reader)
            reader.skip(2)
            obj["seer_quests"].append({"quest": quest, "reward": reward})

        obj["seer_recurring_quests"] = []
        for _ in range(reader.u32()):
            quest = read_quest(reader)
            reward = read_reward(reader)
            reader.skip(2)
            obj["seer_recurring_quests"].append({"quest": quest, "reward": reward})

        first = (obj["seer_quests"] or obj["seer_recurring_quests"] or [None])[0]
        if first:
            obj["quest"] = first["quest"]
            obj["reward"] = first["reward"]
    else:
        obj["quest"] = read_quest(reader)
        obj["reward"] = read_reward(reader)
        reader.skip(2)


def read_shrine_object(reader, obj):
    """Дочитывает shrine: ID заклинания, которому он учит."""
    obj["spell"] = read_spell32(reader)


def read_sign_object(reader, obj):
    """Дочитывает табличку или океанскую бутылку с текстом."""
    obj["message"] = reader.string()
    reader.skip(4)


def read_scroll_object(reader, obj):
    """Дочитывает свиток: сообщение/охрану и ID заклинания."""
    obj["guardians"] = read_message_and_guards(reader)
    obj["spell"] = read_spell32(reader)


def read_town_object(reader, obj, info):
    """Дочитывает город: владельца, гарнизон, постройки и магическую гильдию."""
    building_bytes = town_building_bytes(info)
    obj["object_id"] = reader.u32()
    obj["owner"] = read_player(reader)
    if reader.bool():
        obj["name"] = reader.string()
    if reader.bool():
        obj["garrison"] = read_creatures(reader)
    obj["formation"] = reader.u8()
    if reader.bool():
        built_raw = list(reader.bytes(building_bytes))
        disabled_raw = list(reader.bytes(building_bytes))
        obj["built"] = decode_buildings(built_raw)
        obj["disabled_buildings"] = decode_buildings(disabled_raw)
    else:
        obj["has_fort"] = reader.bool()
        obj["built"] = {"DEFAULT"}
        obj["disabled_buildings"] = set()
    obj["must_spells"], _ = bitmask(reader, 9, 70)
    obj["may_not_spells"], _ = bitmask(reader, 9, 70)
    obj["spell_research"] = reader.bool()
    obj["events"] = [read_town_event(reader, building_bytes, is_hota_v3(info)) for _ in range(reader.u32())]
    obj["alignment"] = reader.u8()
    reader.skip(3)


def read_owner32_object(reader, obj):
    """Дочитывает простые объекты, где payload состоит из 32-битного владельца."""
    obj["owner"] = read_player32(reader)


def read_abandoned_mine_object(reader, obj):
    """Дочитывает заброшенную шахту и маску возможных ресурсов."""
    obj["resources_mask"], _ = bitmask(reader, 4, 7)


def read_witch_object(reader, obj):
    """Дочитывает Witch Hut: список возможных secondary skills."""
    obj["skills"], _ = bitmask(reader, 4, 29)


OBJECT_PAYLOAD_READERS = {
    "artifact": lambda reader, obj, info: read_artifact_object(reader, obj),
    "bank": read_bank_object,
    "event": read_event_object,
    "garrison": lambda reader, obj, info: read_garrison_object(reader, obj),
    "grail": lambda reader, obj, info: read_grail_object(reader, obj),
    "hero": read_hero_object,
    "monster": read_monster_object,
    "pandora": read_pandora_object,
    "hero_placeholder": lambda reader, obj, info: read_hero_placeholder_object(reader, obj),
    "quest_guard": lambda reader, obj, info: read_quest_guard_object(reader, obj),
    "random_dwelling": lambda reader, obj, info: read_random_dwelling_object(reader, obj),
    "random_dwelling_level": lambda reader, obj, info: read_random_dwelling_level_object(reader, obj),
    "random_dwelling_faction": lambda reader, obj, info: read_random_dwelling_faction_object(reader, obj),
    "resource": lambda reader, obj, info: read_resource_object(reader, obj),
    "scholar": lambda reader, obj, info: read_scholar_object(reader, obj),
    "seer": read_seer_object,
    "shrine": lambda reader, obj, info: read_shrine_object(reader, obj),
    "sign": lambda reader, obj, info: read_sign_object(reader, obj),
    "scroll": lambda reader, obj, info: read_scroll_object(reader, obj),
    "town": read_town_object,
    "owner32": lambda reader, obj, info: read_owner32_object(reader, obj),
    "abandoned_mine": lambda reader, obj, info: read_abandoned_mine_object(reader, obj),
    "witch": lambda reader, obj, info: read_witch_object(reader, obj),
}


def read_victory_artifact(reader):
    read_artifact(reader)


def read_victory_creature(reader):
    read_creature(reader)
    reader.i32()


def read_victory_resource(reader):
    reader.u8()
    reader.i32()


def read_victory_hero(reader):
    reader.coord()
    reader.u8()
    reader.u8()


def read_victory_coord(reader):
    reader.coord()


def read_victory_none(reader):
    pass


def read_victory_flag_and_coord(reader):
    reader.u8()
    reader.coord()


VICTORY_READERS = {
    0: read_victory_artifact,
    1: read_victory_creature,
    2: read_victory_resource,
    3: read_victory_hero,
    4: read_victory_coord,
    5: read_victory_coord,
    6: read_victory_coord,
    7: read_victory_coord,
    8: read_victory_none,
    9: read_victory_none,
    10: read_victory_flag_and_coord,
}

LOSS_READERS = {
    0: lambda reader: reader.coord(),
    1: lambda reader: reader.coord(),
    2: lambda reader: reader.i16(),
}


def read_object(reader, templates, index, info):
    """Читает один объект карты и передает его payload нужному обработчику."""
    start = reader.tell()
    position = reader.coord()
    template_index = reader.u32()
    reader.skip(5)
    template = templates[template_index]
    object_class = template["class"]
    subtype = template["subtype"]
    kind = property_type(object_class, subtype)
    obj = {
        "index": index,
        "position": position,
        "template": template_index,
        "class": object_class,
        "subtype": subtype,
        "def": template["def"],
        "kind": kind,
        "active": active_tiles(position, template["active_raw"]),
    }
    try:
        if kind != "none":
            OBJECT_PAYLOAD_READERS[kind](reader, obj, info)
    except Exception as exc:
        raise RuntimeError(
            f"object {index} at {start}, pos={position}, class={object_class}, "
            f"subtype={subtype}, def={template['def']}, kind={kind}"
        ) from exc
    obj["end"] = reader.tell()
    return obj


def read_objects(reader, templates, info, object_count=None):
    """Читает последовательную таблицу объектов из H3M."""
    count = reader.u32() if object_count is None else object_count
    return [read_object(reader, templates, index, info) for index in range(count)]


SCAN_CLASSES = {
    5, 6, 16, 24, 25, 26, 34, 43, 44, 45, 54, 62, 65, 66, 67, 68, 69, 70, 71, 72,
    73, 74, 75, 81, 83, 84, 85, 88, 89, 90, 93, 98, 162, 163, 164,
}


def scan_objects(data, templates, info, object_start):
    """Сканирует файл побайтно и достает объекты, если таблица не читается подряд."""
    objects = []
    seen_offsets = set()
    for offset in range(object_start, len(data) - 12):
        template_index = struct.unpack_from("<I", data, offset + 3)[0]
        if (
            data[offset] >= info["size"]
            or data[offset + 1] >= info["size"]
            or data[offset + 2] >= info["levels"]
            or template_index >= len(templates)
            or data[offset + 7 : offset + 12] != b"\x00\x00\x00\x00\x00"
        ):
            continue

        if templates[template_index]["class"] not in SCAN_CLASSES:
            continue

        reader = Reader(data)
        reader.offset = offset
        try:
            obj = read_object(reader, templates, len(objects), info)
        except Exception:
            continue

        if reader.tell() <= offset + 12 or reader.tell() > len(data):
            continue

        key = (offset, reader.tell(), obj["class"], obj["subtype"], obj["position"])
        if key in seen_offsets:
            continue

        seen_offsets.add(key)
        obj["scan_offset"] = offset
        objects.append(obj)

    return objects


def parse_map_full(path):
    """Пытается разобрать карту последовательно, от заголовка до глобальных событий."""
    reader = Reader(gzip.open(path, "rb").read())
    info, reader = read_minimal_header(reader.data)
    info["parser_mode"] = "full"

    players = []
    for player_id in range(8):
        player = {
            "id": player_id,
            "can_human": reader.bool(),
            "can_computer": reader.bool(),
        }
        player["behavior"] = reader.i8()
        player["faction_selectable"] = reader.u8()
        player["allowed_factions"], _ = bitmask(reader, 2, 10)
        player["random_faction"] = reader.bool()
        if reader.bool():
            player["generate_hero"] = reader.bool()
            player["main_town_type"] = reader.u8()
            player["main_town_coord"] = reader.coord()
        player["has_random_heroes"] = reader.bool()
        hero = read_hero(reader)
        player["starting_hero"] = hero
        if hero is not None:
            player["starting_hero_portrait"] = read_hero(reader)
            player["starting_hero_name"] = reader.string()
        player["num_placeholder"] = reader.u8()
        player["custom_hero_names"] = [(read_hero(reader), reader.string()) for _ in range(reader.u32())]
        players.append(player)
    info["players"] = players

    victory = reader.u8()
    if victory != 0xFF:
        reader.bool()
        reader.bool()
        try:
            VICTORY_READERS[victory](reader)
        except KeyError as exc:
            raise ValueError(f"unsupported victory condition {victory}") from exc

    loss = reader.u8()
    if loss != 0xFF:
        try:
            LOSS_READERS[loss](reader)
        except KeyError as exc:
            raise ValueError(f"unsupported loss condition {loss}") from exc

    teams = reader.u8()
    if teams:
        for player in players:
            player["team"] = reader.u8()

    hero_count = reader.u32()
    info["starting_hero_count"] = hero_count
    info["starting_heroes"], _ = bitmask(reader, (hero_count + 7) // 8, hero_count)
    info["placeholder_heroes"] = [read_hero(reader) for _ in range(reader.u32())]
    info["custom_heroes"] = []
    for _ in range(reader.u8()):
        info["custom_heroes"].append(
            {
                "hero": read_hero(reader),
                "portrait": read_hero(reader),
                "name": reader.string(),
                "players": bitmask(reader, 1, 8)[0],
            }
        )

    reader.skip(31)
    info["special_weeks"] = reader.bool()
    reader.skip(3)
    info["hota_unknown16"] = reader.u16()
    reader.skip(4)
    artifact_count = reader.u32()
    info["artifact_count_decl"] = artifact_count
    info["unavailable_artifacts"], _ = bitmask(reader, (artifact_count + 7) // 8, artifact_count)
    info["unavailable_spells"], _ = bitmask(reader, 9, 70)
    info["unavailable_skills"], _ = bitmask(reader, 4, 29)

    info["rumors"] = [(reader.string(), reader.string()) for _ in range(reader.u32())]
    hero_count = reader.u32()
    info["hero_count_decl"] = hero_count
    predefined = []
    for hero_id in range(hero_count):
        if not reader.bool():
            continue
        hero = {"id": hero_id}
        if reader.bool():
            hero["experience"] = reader.u32()
        if reader.bool():
            hero["skills"] = [read_secondary(reader) for _ in range(reader.u32())]
        hero["artifacts"] = read_hero_artifacts_if_present(reader, is_hota_v3(info))
        if reader.bool():
            hero["biography"] = reader.string()
        hero["gender"] = reader.i8()
        if reader.bool():
            hero["spells"], _ = bitmask(reader, 9, 70)
        if reader.bool():
            hero["primary"] = read_primary(reader)
        predefined.append(hero)
    info["predefined_heroes"] = predefined

    tiles = []
    for z in range(info["levels"]):
        level = []
        for y in range(info["size"]):
            row = []
            for x in range(info["size"]):
                row.append(tuple(reader.bytes(7)))
            level.append(row)
        tiles.append(level)
    info["tiles"] = tiles

    templates = read_templates(reader)
    info["templates_count"] = len(templates)

    objects = read_objects(reader, templates, info)

    info["objects_count"] = len(objects)
    info["global_events"] = [read_timed_event(reader, is_hota_v3(info)) for _ in range(reader.u32())]
    info["final_offset"] = reader.tell()
    info["data_len"] = len(reader.data)
    info["padding_left"] = len(reader.data) - reader.tell()
    return {"info": info, "templates": templates, "objects": objects}


def parse_map_objects_fallback(path, parse_error):
    """Восстанавливает объектный слой, когда полный разбор HotA-заголовка не удался."""
    data = gzip.open(path, "rb").read()
    info, _reader = read_minimal_header(data)
    info["parser_mode"] = "objects_fallback"
    info["full_parse_error"] = f"{type(parse_error).__name__}: {parse_error}"
    info["players"] = []
    info["unavailable_spells"] = set()
    info["unavailable_artifacts"] = set()
    info["unavailable_skills"] = set()

    template_offset, templates, object_count, object_start = find_template_offset(
        data,
        info["size"],
        info["levels"],
    )
    reader = Reader(data)
    reader.offset = object_start
    try:
        objects = read_objects(reader, templates, info, object_count)
    except Exception as exc:
        info["parser_mode"] = "objects_scan_fallback"
        info["object_table_parse_error"] = f"{type(exc).__name__}: {exc}"
        objects = scan_objects(data, templates, info, object_start)

    info["tiles_offset_estimate"] = template_offset - info["size"] * info["size"] * info["levels"] * 7
    info["declared_objects_count"] = object_count
    info["templates_offset"] = template_offset
    info["templates_count"] = len(templates)
    info["objects_count"] = len(objects)
    info["global_events"] = []
    info["final_offset"] = max([obj.get("end", object_start) for obj in objects], default=object_start)
    info["data_len"] = len(data)
    info["padding_left"] = len(data) - reader.tell()
    return {"info": info, "templates": templates, "objects": objects}


def parse_map(path):
    """Разбирает карту полным способом или переходит к объектному fallback."""
    try:
        return parse_map_full(path)
    except OSError:
        raise
    except Exception as exc:
        return parse_map_objects_fallback(path, exc)


def distance(a, b):
    """Считает расстояние между клетками с большим штрафом за другой этаж."""
    return max(abs(a[0] - b[0]), abs(a[1] - b[1])) + (1000 if a[2] != b[2] else 0)


def point(obj):
    """Возвращает игровую активную клетку объекта, а если ее нет - позицию объекта."""
    return obj["active"][0] if obj["active"] else obj["position"]


def coord_text(value):
    """Форматирует координату для печати в консоль."""
    return f"({value[0]}, {value[1]}, {value[2]})"


def parse_spell_arg(value):
    """Преобразует имя или номер заклинания из аргумента командной строки в spell_id."""
    lowered = value.strip().lower()
    for spell, name in SPELL_NAMES.items():
        if lowered == name.lower() or lowered == str(spell):
            return spell

    matches = [spell for spell, name in SPELL_NAMES.items() if lowered in name.lower()]
    if len(matches) == 1:
        return matches[0]

    raise ValueError(f"unknown or ambiguous spell: {value}")


def parse_artifact_arg(value):
    """Преобразует имя или номер артефакта из аргумента командной строки в artifact_id."""
    lowered = value.strip().lower()
    if lowered.startswith("0x"):
        return int(lowered, 16)
    if lowered.isdigit():
        return int(lowered)
    if lowered in ARTIFACT_ALIASES:
        return ARTIFACT_ALIASES[lowered]

    for artifact, name in ARTIFACT_NAMES.items():
        if lowered == name.lower() or lowered in name.lower():
            return artifact

    matches = [artifact for name, artifact in ARTIFACT_ALIASES.items() if lowered in name]
    if len(set(matches)) == 1:
        return matches[0]

    raise ValueError(f"unknown or ambiguous artifact: {value}")


def parse_hero_arg(value):
    """Преобразует имя или номер героя из аргумента командной строки в hero_id."""
    lowered = value.strip().lower()
    if lowered.startswith("0x"):
        return int(lowered, 16)
    if lowered.isdigit():
        return int(lowered)
    if lowered in HERO_ALIASES:
        return HERO_ALIASES[lowered]

    for hero, name in HERO_NAMES.items():
        if lowered == name.lower() or lowered in name.lower():
            return hero

    matches = [hero for name, hero in HERO_ALIASES.items() if lowered in name]
    if len(set(matches)) == 1:
        return matches[0]

    raise ValueError(f"unknown or ambiguous hero: {value}")


def artifact_name(artifact):
    """Возвращает имя артефакта или запасной текст с его ID."""
    return ARTIFACT_NAMES.get(artifact, f"artifact #{artifact}")


def hero_name(hero):
    """Возвращает имя героя или запасной текст с его ID."""
    return HERO_NAMES.get(hero, f"hero #{hero}")


def event_spells_reliable(obj):
    """Отсекает явно сломанные списки заклинаний из fallback-сканирования."""
    spells = obj.get("event", {}).get("spells", [])
    return all(spell in SPELL_NAMES for spell in spells)


def seer_rewards(obj):
    """Собирает все награды Seer's Hut в единый список для поиска."""
    items = []
    if "reward" in obj:
        items.append({"quest": obj.get("quest"), "reward": obj.get("reward")})
    items.extend(obj.get("seer_quests", []))
    items.extend(obj.get("seer_recurring_quests", []))
    return items


def spell_sources(objects, wanted_spell):
    """Ищет все известные источники заданного заклинания среди объектов карты."""
    sources = []
    for obj in objects:
        event = obj.get("event", {})
        if obj["kind"] == "shrine" and obj.get("spell") == wanted_spell:
            sources.append(("shrine", obj))
        if obj["kind"] == "scroll" and obj.get("spell") == wanted_spell:
            sources.append(("scroll", obj))
        if obj["kind"] == "scholar" and obj.get("reward_type") == 2 and obj.get("reward") == wanted_spell:
            sources.append(("scholar", obj))
        if obj["kind"] == "seer":
            for item in seer_rewards(obj):
                reward = item.get("reward", {})
                if reward.get("type") == 9 and reward.get("value") == wanted_spell:
                    sources.append(("seer", obj))
                    break
        if obj["kind"] in ("event", "pandora") and event_spells_reliable(obj) and wanted_spell in event.get("spells", []):
            sources.append((obj["kind"], obj))
        if obj["kind"] == "town" and wanted_spell in obj.get("must_spells", set()):
            sources.append(("town-forced-guild", obj))
    return sources


def hero_artifact_source_type(obj):
    """Называет способ получить артефакт, если он находится у героя."""
    if obj["class"] == 34:
        return "defeat-hero"
    if obj["class"] == 62:
        return "hero-camp-carried" if is_hero_camp(obj) else "prison-hero-carried"
    return "hero-carried"


def hero_carries_artifact(obj, wanted_artifact):
    """Проверяет артефакты героя, не доверяя сырому backpack из scan fallback."""
    artifacts = obj.get("artifacts")
    if not isinstance(artifacts, dict):
        return False

    equipped = artifacts.get("equipped", [])
    if wanted_artifact in equipped:
        return True

    # In object scan fallback, backpack often contains a raw byte tail after a
    # partial parse. Equipped slots are much more stable, so only full parses use
    # backpack as an artifact source.
    if obj.get("scan_offset") is None and wanted_artifact in artifacts.get("backpack", []):
        return True

    return False


def artifact_sources(objects, wanted_artifact):
    """Ищет известные источники артефакта среди объектов карты."""
    sources = []
    for obj in objects:
        event = obj.get("event", {})
        scan_fallback = obj.get("scan_offset") is not None

        if obj["kind"] == "artifact" and obj["class"] == 5 and obj.get("subtype") == wanted_artifact:
            sources.append(("map-artifact", obj))

        if obj["kind"] in ("event", "pandora") and wanted_artifact in event.get("artifacts", []):
            sources.append((obj["kind"], obj))

        if obj["kind"] == "seer":
            for item in seer_rewards(obj):
                reward = item.get("reward", {})
                if reward.get("type") == 8 and reward.get("value") == wanted_artifact:
                    sources.append(("seer", obj))
                    break

        if not scan_fallback and obj["kind"] == "monster" and obj.get("artifact") == wanted_artifact:
            sources.append(("monster-reward", obj))

        if not scan_fallback and obj["kind"] == "bank" and wanted_artifact in obj.get("artifacts", []):
            sources.append(("creature-bank", obj))

        if obj["kind"] == "hero" and hero_carries_artifact(obj, wanted_artifact):
            sources.append((hero_artifact_source_type(obj), obj))

    return sources


def hero_sources(objects, wanted_hero):
    """Ищет героя среди всех геройских объектов: на карте, в тюрьме или random hero."""
    return [
        obj
        for obj in objects
        if obj["kind"] == "hero" and (obj.get("hero") == wanted_hero or obj.get("name", "").lower() == hero_name(wanted_hero).lower())
    ]


def hero_source_type(obj):
    """Называет место, где лежит герой, без предположения что это всегда тюрьма."""
    if obj["class"] == 62:
        return "hero-camp" if is_hero_camp(obj) else "prison"
    if obj["class"] == 34:
        return "map-hero"
    if obj["class"] == 70:
        return "random-hero"
    return "hero"


def is_hero_camp(obj):
    """Отличает Hero Camp от обычной тюрьмы по subtype или имени def."""
    return obj["class"] == 62 and (obj.get("subtype") == 1 or "hcamp" in obj.get("def", "").lower())


def is_prison(obj):
    """Проверяет, что объект class 62 является именно Prison, а не Hero Camp."""
    return obj["class"] == 62 and not is_hero_camp(obj)


def prison_objects(objects):
    """Возвращает все тюрьмы с героями."""
    return [obj for obj in objects if obj["kind"] == "hero" and is_prison(obj)]


def camp_objects(objects):
    """Возвращает все лагеря героев."""
    return [obj for obj in objects if obj["kind"] == "hero" and is_hero_camp(obj)]


def looks_readable_hero_name(value):
    """Отсекает битые имена из fallback-сканирования."""
    if not value:
        return False
    return any(
        "a" <= ch.lower() <= "z"
        or "\u0400" <= ch <= "\u04ff"
        or ch.isdigit()
        for ch in value
    )


def display_hero_name(obj):
    """Выбирает кастомное имя героя или имя по ID, если кастомное выглядит битым."""
    name = obj.get("name")
    if looks_readable_hero_name(name):
        return name
    return hero_name(obj.get("hero"))


def object_name(obj):
    """Строит короткое человекочитаемое имя объекта для вывода."""
    base = OBJ_NAMES.get(obj["class"], obj["kind"])
    if is_hero_camp(obj):
        base = "Hero Camp"
    if obj["kind"] == "artifact" and obj["class"] == 5:
        return f"{base}: {artifact_name(obj.get('subtype'))}"
    if obj["kind"] == "hero":
        return f"{base}: {display_hero_name(obj)}"
    if obj["kind"] in ("shrine", "scroll"):
        return f"{base}: {SPELL_NAMES.get(obj.get('spell'), obj.get('spell'))}"
    if obj["kind"] == "scholar":
        return f"{base}: {SPELL_NAMES.get(obj.get('reward'), obj.get('reward'))}"
    if obj["kind"] in ("event", "pandora"):
        spells = [SPELL_NAMES.get(spell, spell) for spell in obj.get("event", {}).get("spells", [])]
        if spells:
            return f"{base}: spells {spells}"
        artifacts = [artifact_name(artifact) for artifact in obj.get("event", {}).get("artifacts", []) if artifact is not None]
        if artifacts:
            return f"{base}: artifacts {artifacts}"
    return base


def serializable(value):
    """Помогает json.dumps печатать множества как отсортированные списки."""
    if isinstance(value, set):
        return sorted(value)
    raise TypeError(type(value).__name__)


def print_usage(stream=sys.stdout):
    """Печатает короткую подсказку по запуску без traceback."""
    print(
        "Использование:\n"
        "  python analyze_h3m.py \"<map.h3m>\" summary\n"
        "  python analyze_h3m.py \"<map.h3m>\" spell \"Town Portal\"\n"
        "  python analyze_h3m.py \"<map.h3m>\" artifact \"Golden Bow\"\n"
        "  python analyze_h3m.py \"<map.h3m>\" hero \"Gelu\"\n"
        "  python analyze_h3m.py \"<map.h3m>\" prisons\n"
        "  python analyze_h3m.py \"<map.h3m>\" camps\n"
        "  python analyze_h3m.py \"<map.h3m>\" debug",
        sep="",
        file=stream,
    )


def parser_mode_text(mode):
    """Переводит внутренний режим парсера в короткий текст для пользователя."""
    return {
        "full": "полный разбор",
        "objects_fallback": "таблица объектов",
        "objects_scan_fallback": "сканирование объектов",
    }.get(mode, mode or "неизвестно")


def print_summary(info, objects, red_ref):
    """Печатает короткую сводку без внутренней отладочной простыни."""
    town_portal_unavailable = TOWN_PORTAL_SPELL_ID in info.get("unavailable_spells", set())
    print(f"Карта: {info['name']}")
    print(f"Размер: {info['size']}x{info['size']}, этажей: {info['levels']}")
    print(f"Режим чтения: {parser_mode_text(info.get('parser_mode'))}")
    print(f"Шаблонов объектов: {info['templates_count']}")
    print(f"Объектов найдено: {info['objects_count']}")
    print(f"Town Portal глобально запрещен: {'да' if town_portal_unavailable else 'нет'}")
    if red_ref is not None:
        print(f"Стартовый город красного: {coord_text(red_ref)}")


def print_debug(info, objects, red_ref):
    """Печатает подробный JSON для отладки парсера."""
    print(
        json.dumps(
            {
                "info": {
                    "name": info["name"],
                    "hota_format1": info["hota_format1"],
                    "hota_format2": info["hota_format2"],
                    "size": info["size"],
                    "levels": info["levels"],
                    "parser_mode": info.get("parser_mode"),
                    "full_parse_error": info.get("full_parse_error"),
                    "object_table_parse_error": info.get("object_table_parse_error"),
                    "templates_count": info["templates_count"],
                    "declared_objects_count": info.get("declared_objects_count"),
                    "objects_count": info["objects_count"],
                    "padding_left": info["padding_left"],
                    "town_portal_unavailable": TOWN_PORTAL_SPELL_ID in info.get("unavailable_spells", set()),
                },
                "red_reference": red_ref,
                "object_classes": Counter(obj["class"] for obj in objects).most_common(20),
            },
            indent=2,
            ensure_ascii=False,
            default=serializable,
        )
    )


def print_sources(title, sources):
    """Печатает список найденных объектов с координатами."""
    print(title)
    for source_type, obj in sources:
        print(
            f"{source_type:17s} #{obj['index']:5d} active={coord_text(point(obj))} "
            f"pos={coord_text(obj['position'])} {object_name(obj)}"
        )


def print_hero_sources(wanted_hero, objects):
    """Печатает все объектные места, где найден заданный герой."""
    sources = hero_sources(objects, wanted_hero)
    print(f"{hero_name(wanted_hero)} sources: {len(sources)}")
    for obj in sources:
        source_type = hero_source_type(obj)
        print(
            f"{source_type:17s} #{obj['index']:5d} active={coord_text(point(obj))} "
            f"pos={coord_text(obj['position'])} {object_name(obj)}"
        )


def print_prisons(objects):
    """Печатает все найденные тюрьмы."""
    prisons = prison_objects(objects)
    print(f"Prisons: {len(prisons)}")
    for obj in prisons:
        print(
            f"prison            #{obj['index']:5d} active={coord_text(point(obj))} "
            f"pos={coord_text(obj['position'])} {object_name(obj)}"
        )


def print_camps(objects):
    """Печатает все найденные лагеря героев."""
    camps = camp_objects(objects)
    print(f"Hero Camps: {len(camps)}")
    for obj in camps:
        print(
            f"hero-camp         #{obj['index']:5d} active={coord_text(point(obj))} "
            f"pos={coord_text(obj['position'])} {object_name(obj)}"
        )


def main():
    """Точка входа CLI: summary, spell, artifact, hero, prisons, camps или debug."""
    if len(sys.argv) < 2:
        print_usage()
        return 2

    path = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else "summary"
    if command not in ("summary", "spell", "artifact", "hero", "prisons", "camps", "debug"):
        print(f"Неизвестная команда: {command}", file=sys.stderr)
        print_usage(sys.stderr)
        return 2

    try:
        wanted_spell = parse_spell_arg(sys.argv[3]) if command == "spell" and len(sys.argv) > 3 else TOWN_PORTAL_SPELL_ID
        wanted_artifact = parse_artifact_arg(sys.argv[3]) if command == "artifact" and len(sys.argv) > 3 else None
        wanted_hero = parse_hero_arg(sys.argv[3]) if command == "hero" and len(sys.argv) > 3 else None
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2

    if command in ("artifact", "hero") and len(sys.argv) < 4:
        print(f"Для команды {command} нужен аргумент.", file=sys.stderr)
        print_usage(sys.stderr)
        return 2

    try:
        data = parse_map(path)
    except FileNotFoundError:
        print(f"Файл карты не найден: {path}", file=sys.stderr)
        print_usage(sys.stderr)
        return 1
    except OSError as exc:
        print(f"Не удалось прочитать карту {path}: {exc}", file=sys.stderr)
        return 1

    info = data["info"]
    objects = data["objects"]
    red = next((player for player in info.get("players", []) if player["id"] == 0), None)
    red_ref = red.get("main_town_coord") if red else None

    if command == "summary":
        print_summary(info, objects, red_ref)
        return 0

    if command == "debug":
        print_debug(info, objects, red_ref)
        return 0

    if command == "spell":
        sources = spell_sources(objects, wanted_spell)
        print_sources(f"{SPELL_NAMES.get(wanted_spell, wanted_spell)} sources: {len(sources)}", sources)
        return 0

    if command == "artifact":
        sources = artifact_sources(objects, wanted_artifact)
        print_sources(f"{artifact_name(wanted_artifact)} sources: {len(sources)}", sources)
        return 0

    if command == "hero":
        print_hero_sources(wanted_hero, objects)
        return 0

    if command == "prisons":
        print_prisons(objects)
        return 0

    if command == "camps":
        print_camps(objects)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
