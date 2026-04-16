from model import Check
from enums import Scene as S, Items as I, Songs, Masks as M, Remains as R, Events as E, TimeSlot as T
from dungeons import room_node, small_key, WFT_SK1

CHECKS: dict[str, Check] = {}

# Shorthand for time windows
N = None                                        # any time
D1 = frozenset({T.DAY_1})
N1 = frozenset({T.NIGHT_1})
D2 = frozenset({T.DAY_2})
N2 = frozenset({T.NIGHT_2})
D3 = frozenset({T.DAY_3})
N3 = frozenset({T.NIGHT_3})
ANY_DAY = frozenset({T.DAY_1, T.DAY_2, T.DAY_3})
ANY_NIGHT = frozenset({T.NIGHT_1, T.NIGHT_2, T.NIGHT_3})
D1_D2 = frozenset({T.DAY_1, T.DAY_2})


def check(id, scene, requires=None, time=N, duration=0, warp_to=None):
    c = Check(id, scene, requires or set(), time, duration, warp_to)
    CHECKS[id] = c
    return c


# =============================================================================
# Glitchless — Full item/mask/upgrade list with time constraints
# =============================================================================

# =====================
# === CLOCK TOWN
# =====================
check(I.StrayFairyCT,    S.LaundryPool)
check(I.Magic,           S.CTGreatFairyFountain,  {I.StrayFairyCT})
check(I.Ocarina,         S.ClockTowerRooftop,     {I.Magic},               N3)  # midnight Night 3
check(Songs.Time,        S.ClockTowerRooftop,     {I.Ocarina},             N3)
check(Songs.Healing,     S.ClockTowerInterior,    {I.Ocarina, Songs.Time})
check(M.Deku,            S.ClockTowerInterior,    {Songs.Healing})
check(I.BombBag,         S.WestClockTown)
check(M.GreatFairy,      S.CTGreatFairyFountain,  {I.Magic, M.Deku})
check(M.Blast,           S.NorthClockTown,        {M.Deku},                N1)  # save old lady midnight Night 1
check(M.KafeiMask,       S.EastClockTown,         {M.Deku})
check(M.Bremen,          S.LaundryPool,           {M.Deku},                ANY_NIGHT)
check(M.Kamaro,          S.TerminaField,          {Songs.Healing},         ANY_NIGHT)
check(M.AllNight,        S.WestClockTown,         {M.Blast},               N3)  # Curiosity Shop Night 3
check(I.AdultWallet,     S.WestClockTown)
check(I.BombersNotebook, S.EastClockTown,         {M.Deku, I.Magic})
check(I.MoonsTear,       S.Observatory,           {I.Magic})
check(I.RoomKey,         S.EastClockTown,         {M.Deku})

# =====================
# === SONG OF SOARING
# =====================
check(Songs.Soaring,     S.SouthernSwamp,         {I.Ocarina})

# =====================
# === BOTTLES
# =====================
check(I.Bottle,          S.SouthernSwamp,         {M.Deku})
check(I.BottleAliens,    S.RomaniRanch,           {I.Bow, I.Epona},        N1)  # aliens attack ~2:30 AM Night 1
check(I.GoldDust,        S.GoronRacetrack,        {M.Goron, R.Goht})
check(I.BottleGoldDust,  S.WestClockTown,         {I.GoldDust},            ANY_NIGHT)  # Curiosity Shop after 10 PM
check(I.BottleGraveyard, S.IkanaGraveyard,        {I.Bow, M.Captain},      N3)
check(I.BottleBeaver,    S.ZoraCape,              {M.Zora, I.Hookshot})

# =====================
# === SOUTHERN SWAMP / WOODFALL
# =====================
check(I.MagicBeans,      S.DekuPalace)
check(Songs.Sonata,      S.DekuPalace,            {M.Deku})
# WFT room-level checks
_WFT = S.WoodfallTemple
check(WFT_SK1,     room_node(_WFT, 5),      {Songs.Sonata, M.Deku, I.Magic})  # small key in Room 5
check(I.Bow,             room_node(_WFT, 7),      {WFT_SK1})                  # bow in Room 7, key unlocks path
check(I.BossKeyWFT,      room_node(_WFT, 8),      {I.Bow})                          # frog fight in Room 8
check(R.Odolwa,          room_node(_WFT, "Boss"),  {I.BossKeyWFT},
      duration=180, warp_to=S.DekuPrincessPrison)                                    # 3 min: boss -> GC -> prison
check(Songs.OathToOrder, S.DekuPrincessPrison,     {R.Odolwa})                        # learned in GC during boss CS
# Deku Princess: catch in bottle at prison after Odolwa, release in king's chamber as Deku
check(I.DekuPrincess,    S.DekuPrincessPrison,    {R.Odolwa, I.Bottle})              # need empty bottle
check(M.Scents,          S.DekuPalace,            {I.DekuPrincess, M.Deku})           # release princess -> butler race
check(M.Truth,           S.SwampSpiderHouse,      {M.Deku, I.Bottle, I.Bow})   # need bow (or stick) to enter, all 30 skulltulas
check(I.SpinAttack,      S.Woodfall,              {R.Odolwa})

# =====================
# === MOUNTAIN / SNOWHEAD
# =====================
check(I.LensOfTruth,     S.LonePeakShrine,        {I.Magic, I.Bow, I.BombBag})
check(M.Goron,           S.MountainVillage,        {I.LensOfTruth, Songs.Healing}, duration=90)  # 90s cutscene
check(M.DonGero,         S.MountainVillage,        {M.Goron})
check(Songs.LullabyIntro,S.GoronVillage,           {M.Goron})
check(Songs.Lullaby,     S.GoronShrine,            {Songs.LullabyIntro, M.Goron})
check(I.FireArrows,      S.SnowheadTemple,         {Songs.Lullaby, M.Goron, I.Magic})
check(I.BossKeySHT,      S.SnowheadTemple,         {I.FireArrows})
check(R.Goht,            S.SnowheadTemple,         {I.BossKeySHT},          duration=120, warp_to=S.MountainVillage)  # 2 min: boss -> GC -> mtn village
check(I.DoubleMagic,     S.Snowhead,               {R.Goht})
check(I.RazorSword,      S.MountainVillage,        {I.FireArrows})
check(I.GildedSword,     S.MountainVillage,        {I.RazorSword, I.GoldDust})
check(I.PowderKeg,       S.GoronVillage,           {M.Goron, I.FireArrows})
check(I.Epona,           S.RomaniRanch,            {I.PowderKeg})

# =====================
# === MILK ROAD / RANCH
# =====================
check(M.BunnyHood,       S.RomaniRanch,            {M.Bremen, I.Epona})
check(M.Romani,          S.RomaniRanch,            {I.BottleAliens},        N2)  # Cremia milk delivery Night 2

# =====================
# === GREAT BAY
# =====================
check(M.Zora,            S.GreatBayCoast,          {Songs.Healing, I.Epona}, duration=90)  # 90s cutscene
check(I.Hookshot,        S.PiratesFortress,        {M.Zora})
check(Songs.NewWave,     S.MarineResearchLab,      {M.Zora, I.Hookshot, I.Bottle, I.BottleAliens, I.BottleGoldDust})
check(I.IceArrows,       S.GreatBayTemple,         {Songs.NewWave, M.Zora})
check(I.BossKeyGBT,      S.GreatBayTemple,         {I.IceArrows})
check(R.Gyorg,           S.GreatBayTemple,         {I.BossKeyGBT},          duration=120, warp_to=S.ZoraCape)  # 2 min: boss -> GC -> zora cape
check(I.EnhancedDefense, S.ZoraCape,               {R.Gyorg})
check(I.GiantWallet,     S.OceanSpiderHouse,       {I.Epona},               D1)  # must be Day 1

# =====================
# === IKANA / STONE TOWER
# =====================
check(M.Garo,            S.GormanTrack,            {I.Epona},               D1_D2)  # Day 1 or Day 2
check(M.Stone,           S.IkanaTrail,             {I.LensOfTruth, I.Bottle})
check(M.Captain,         S.IkanaGraveyard,         {Songs.Sonata, M.Garo, I.Hookshot})
check(Songs.Storms,      S.IkanaGraveyard,         {M.Captain})
check(M.Gibdo,           S.IkanaCanyon,            {Songs.Storms, Songs.Healing})
check(I.MirrorShield,    S.BeneathTheWell,         {M.Gibdo, I.BombBag, I.Bottle, I.MagicBeans, I.Epona})
check(Songs.Elegy,       S.IkanaCastle,            {I.MirrorShield, I.PowderKeg})
check(I.LightArrows,     S.StoneTowerTemple,       {Songs.Elegy, M.Goron, M.Zora, M.Deku})
check(M.Giant,           S.StoneTowerTemple,       {I.LightArrows})
check(I.BossKeySTT,      S.StoneTowerTemple,       {I.LightArrows})
check(R.Twinmold,        S.StoneTowerTemple,       {I.BossKeySTT, M.Giant}, duration=120, warp_to=S.IkanaCanyon)  # 2 min: boss -> GC -> ikana canyon
check(I.GreatFairySword, S.IkanaCanyon,            {R.Twinmold})

# =====================
# === MILK BAR / MULTI-REGION
# =====================
check(M.CircusLeader,    S.EastClockTown,          {M.Romani, M.Deku, M.Goron, M.Zora, I.Ocarina})

# =====================
# === MOON
# =====================
check(E.EnterMoon,       S.ClockTowerRooftop,
      {R.Odolwa, R.Goht, R.Gyorg, R.Twinmold, Songs.OathToOrder, I.Ocarina}, N3)
check(E.KillMajora,      S.TheMoon,               {E.EnterMoon})

# =====================
# === UPGRADES
# =====================
check(I.BombBag30,       S.WestClockTown,          {I.BombBag, M.Blast})
check(I.BombBag40,       S.MountainVillage,        {I.BombBag30, M.Goron})
check(I.Quiver40,        S.EastClockTown,          {I.Bow})
check(I.Quiver50,        S.SouthernSwamp,          {I.Bow, I.Quiver40})

# =====================
# === KAFEI QUEST
# =====================
check(I.LetterToKafei,    S.EastClockTown,    {M.KafeiMask, I.RoomKey},    N1)   # midnight meeting Night 1
check(I.PendantOfMemories,S.LaundryPool,      {I.LetterToKafei},           D2)   # find Kafei Day 2
check(I.PriorityMail,    S.LaundryPool,       {I.PendantOfMemories},       D3)   # hideout Day 3
check(M.Keaton,           S.LaundryPool,       {I.PendantOfMemories},       D3)
# EXCLUSIVE per cycle — can only do one per quest run:
check(M.Postman,          S.WestClockTown,     {I.PriorityMail},            N3)
check(I.BottleMadameAroma,S.EastClockTown,     {I.PriorityMail, M.Romani}, N3)   # Milk Bar
check(M.Couple,           S.EastClockTown,
      {I.PendantOfMemories, M.Garo, I.Hookshot},                            N3)

# =====================
# === FIERCE DEITY
# =====================
check(M.FierceDeity,      S.TheMoon,
      {M.GreatFairy, M.Blast, M.Stone, M.Bremen, M.Kamaro, M.KafeiMask,
       M.AllNight, M.BunnyHood, M.DonGero, M.Scents, M.Truth,
       M.Captain, M.Garo, M.Gibdo, M.Romani, M.CircusLeader, M.Giant,
       M.Keaton, M.Postman, M.Couple, E.EnterMoon})

# TODO: Heart Pieces (52)
