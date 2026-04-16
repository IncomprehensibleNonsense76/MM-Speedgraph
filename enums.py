from enum import IntEnum, StrEnum


class TimeSlot(IntEnum):
    """Phases within a 3-day cycle. Checks with time constraints must be done during one of their allowed slots."""
    DAY_1 = 0
    NIGHT_1 = 1
    DAY_2 = 2
    NIGHT_2 = 3
    DAY_3 = 4
    NIGHT_3 = 5


class LabeledEnum(StrEnum):
    """StrEnum that carries a human-readable label."""
    def __new__(cls, value: str, label: str = ""):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.label = label or value
        return obj


class Scene(LabeledEnum):
    # === Clock Town ===
    SouthClockTown       = ("South Clock Town",)
    NorthClockTown       = ("North Clock Town",)
    EastClockTown        = ("East Clock Town",)
    WestClockTown        = ("West Clock Town",)
    LaundryPool          = ("Laundry Pool",)
    ClockTowerInterior   = ("Clock Tower Interior",)
    ClockTowerRooftop    = ("Clock Tower Rooftop",)
    CTGreatFairyFountain = ("CT Great Fairy Fountain",)

    # === Overworld ===
    TerminaField         = ("Termina Field",)
    Observatory          = ("Observatory",)

    # === Southern Swamp ===
    SouthernSwamp        = ("Southern Swamp",)
    DekuPalace           = ("Deku Palace",)
    Woodfall             = ("Woodfall",)
    WoodfallTemple       = ("Woodfall Temple",)
    WoodsOfMystery       = ("Woods of Mystery",)
    HagsPotionShop       = ("Hags Potion Shop",)
    DekuPrincessPrison   = ("Deku Princess Prison",)
    SwampSpiderHouse     = ("Swamp Spider House",)

    # === Mountain / Snowhead ===
    PathToMountainVillage = ("Path to Mountain Village",)
    MountainVillage      = ("Mountain Village",)
    PathToGoronVillage   = ("Path to Goron Village",)
    GoronVillage         = ("Goron Village",)
    GoronShrine          = ("Goron Shrine",)
    GoronRacetrack       = ("Goron Racetrack",)
    LonePeakShrine       = ("Lone Peak Shrine",)
    PathToSnowhead       = ("Path to Snowhead",)
    Snowhead             = ("Snowhead",)
    SnowheadTemple       = ("Snowhead Temple",)

    # === Milk Road / Ranch ===
    MilkRoad             = ("Milk Road",)
    RomaniRanch          = ("Romani Ranch",)
    GormanTrack          = ("Gorman Track",)

    # === Great Bay ===
    GreatBayCoast        = ("Great Bay Coast",)
    PiratesFortress      = ("Pirates' Fortress",)
    MarineResearchLab    = ("Marine Research Lab",)
    ZoraCape             = ("Zora Cape",)
    GreatBayTemple       = ("Great Bay Temple",)
    PinnacleRock         = ("Pinnacle Rock",)
    OceanSpiderHouse     = ("Ocean Spider House",)

    # === Ikana ===
    IkanaTrail           = ("Ikana Trail",)
    IkanaCanyon          = ("Ikana Canyon",)
    IkanaGraveyard       = ("Ikana Graveyard",)
    BeneathTheWell       = ("Beneath the Well",)
    IkanaCastle          = ("Ikana Castle",)
    StoneTower           = ("Stone Tower",)
    StoneTowerTemple     = ("Stone Tower Temple",)

    # === Special ===
    GiantsChamber        = ("Giants' Chamber",)
    TheMoon              = ("The Moon",)


class Remains(LabeledEnum):
    Odolwa   = ("odolwa_remains",   "Odolwa's Remains")
    Goht     = ("goht_remains",     "Goht's Remains")
    Gyorg    = ("gyorg_remains",    "Gyorg's Remains")
    Twinmold = ("twinmold_remains", "Twinmold's Remains")


class Items(LabeledEnum):
    # === Weapons / Tools ===
    Ocarina         = ("ocarina",            "Ocarina of Time")
    Bow             = ("bow",                "Hero's Bow")
    BombBag         = ("bomb_bag",           "Bomb Bag")
    Hookshot        = ("hookshot",           "Hookshot")
    LensOfTruth     = ("lens_of_truth",      "Lens of Truth")
    FireArrows      = ("fire_arrows",        "Fire Arrows")
    IceArrows       = ("ice_arrows",         "Ice Arrows")
    LightArrows     = ("light_arrows",       "Light Arrows")
    Magic           = ("magic",              "Magic Power")
    PowderKeg       = ("powder_keg",         "Powder Keg")
    MagicBeans      = ("magic_beans",        "Magic Beans")
    MirrorShield    = ("mirror_shield",      "Mirror Shield")
    Epona           = ("epona",              "Epona")

    # === Swords ===
    RazorSword      = ("razor_sword",        "Razor Sword")
    GildedSword     = ("gilded_sword",       "Gilded Sword")

    # === Bottles / Trade ===
    GoldDust        = ("gold_dust",          "Gold Dust")
    Bottle          = ("bottle",             "Bottle (Kotake/Koume)")
    BottleAliens    = ("bottle_aliens",      "Bottle (Aliens)")
    BottleGoldDust  = ("bottle_gold_dust",   "Bottle (Gold Dust)")

    # === Bottles (additional) ===
    BottleGraveyard = ("bottle_graveyard",   "Bottle (Graveyard)")
    BottleBeaver    = ("bottle_beaver",      "Bottle (Beaver Race)")
    BottleMadameAroma = ("bottle_madame_aroma", "Bottle (Madame Aroma)")

    # === Bottle contents ===
    DekuPrincess    = ("deku_princess",      "Deku Princess (Bottle)")  # Kafei quest

    # === Key Items ===
    BombersNotebook = ("bombers_notebook",   "Bombers' Notebook")
    MoonsTear       = ("moons_tear",         "Moon's Tear")
    RoomKey         = ("room_key",           "Room Key")
    LetterToKafei   = ("letter_to_kafei",    "Letter to Kafei")
    PendantOfMemories = ("pendant_of_memories", "Pendant of Memories")
    PriorityMail    = ("priority_mail",      "Priority Mail")

    # === Collectibles ===
    StrayFairyCT    = ("stray_fairy_ct",     "Stray Fairy (Clock Town)")

    # === Boss Keys ===
    BossKeyWFT      = ("boss_key_wft",       "Boss Key (Woodfall)")
    BossKeySHT      = ("boss_key_sht",       "Boss Key (Snowhead)")
    BossKeyGBT      = ("boss_key_gbt",       "Boss Key (Great Bay)")
    BossKeySTT      = ("boss_key_stt",       "Boss Key (Stone Tower)")

    # === Great Fairy Rewards ===
    SpinAttack      = ("spin_attack",        "Great Spin Attack")
    DoubleMagic     = ("double_magic",       "Double Magic")
    EnhancedDefense = ("enhanced_defense",   "Enhanced Defense")
    GreatFairySword = ("great_fairy_sword",  "Great Fairy Sword")

    # === Wallets ===
    AdultWallet     = ("adult_wallet",       "Adult Wallet")
    GiantWallet     = ("giant_wallet",       "Giant Wallet")

    # === Bomb Bag Upgrades ===
    BombBag30       = ("bomb_bag_30",        "Big Bomb Bag (30)")
    BombBag40       = ("bomb_bag_40",        "Biggest Bomb Bag (40)")

    # === Quiver Upgrades ===
    Quiver40        = ("quiver_40",          "Large Quiver (40)")
    Quiver50        = ("quiver_50",          "Largest Quiver (50)")


class Songs(LabeledEnum):
    Time         = ("song_of_time",     "Song of Time")
    Healing      = ("song_of_healing",  "Song of Healing")
    Soaring      = ("song_of_soaring",  "Song of Soaring")
    Sonata       = ("sonata",           "Sonata of Awakening")
    LullabyIntro = ("lullaby_intro",    "Goron Lullaby Intro")
    Lullaby      = ("lullaby",          "Goron Lullaby")
    NewWave      = ("new_wave",         "New Wave Bossa Nova")
    Elegy        = ("elegy",            "Elegy of Emptiness")
    OathToOrder  = ("oath_to_order",    "Oath to Order")
    Storms       = ("song_of_storms",   "Song of Storms")


class Masks(LabeledEnum):
    # === Transformation ===
    Deku         = ("deku_mask",          "Deku Mask")
    Goron        = ("goron_mask",         "Goron Mask")
    Zora         = ("zora_mask",          "Zora Mask")
    FierceDeity  = ("fierce_deity_mask",  "Fierce Deity Mask")

    # === Regular ===
    GreatFairy   = ("great_fairy_mask",   "Great Fairy Mask")
    Blast        = ("blast_mask",         "Blast Mask")
    Stone        = ("stone_mask",         "Stone Mask")
    Bremen       = ("bremen_mask",        "Bremen Mask")
    Kamaro       = ("kamaro_mask",        "Kamaro's Mask")
    KafeiMask    = ("kafei_mask",         "Kafei's Mask")
    AllNight     = ("all_night_mask",     "All-Night Mask")
    BunnyHood    = ("bunny_hood",         "Bunny Hood")
    DonGero      = ("don_gero_mask",      "Don Gero's Mask")
    Scents       = ("mask_of_scents",     "Mask of Scents")
    Truth        = ("mask_of_truth",      "Mask of Truth")
    Captain      = ("captain_hat",        "Captain's Hat")
    Garo         = ("garo_mask",          "Garo's Mask")
    Gibdo        = ("gibdo_mask",         "Gibdo Mask")
    Romani       = ("romani_mask",        "Romani's Mask")
    CircusLeader = ("circus_leader_mask", "Circus Leader's Mask")
    Giant        = ("giant_mask",         "Giant's Mask")

    # === Kafei quest (TODO: add checks later) ===
    Keaton       = ("keaton_mask",        "Keaton Mask")
    Postman      = ("postman_hat",        "Postman's Hat")
    Couple       = ("couple_mask",        "Couple's Mask")


class Events(LabeledEnum):
    EnterMoon  = ("enter_moon",   "Enter the Moon")
    KillMajora = ("kill_majora",  "Defeat Majora")
