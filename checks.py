from model import Check
from enums import Scene as S, Items as I, Songs, Masks as M, Remains as R, Events as E

CHECKS: dict[str, Check] = {}


def check(id, scene, requires=None):
    c = Check(id, scene, requires or set())
    CHECKS[id] = c
    return c


# =============================================================================
# Glitchless Any% — Full item/mask/upgrade list
# =============================================================================

# =====================
# === CLOCK TOWN
# =====================
check(I.StrayFairyCT,    S.LaundryPool)
check(I.Magic,           S.CTGreatFairyFountain,  {I.StrayFairyCT})
check(I.Ocarina,         S.ClockTowerRooftop,     {I.Magic})                # TIME: midnight Night 3
check(Songs.Time,        S.ClockTowerRooftop,     {I.Ocarina})
check(Songs.Healing,     S.ClockTowerInterior,    {I.Ocarina, Songs.Time})
check(M.Deku,            S.ClockTowerInterior,    {Songs.Healing})
check(I.BombBag,         S.WestClockTown)                                   # buy from bomb shop
check(M.GreatFairy,      S.CTGreatFairyFountain,  {I.Magic, M.Deku})        # another cycle, another fairy
check(M.Blast,           S.NorthClockTown,        {M.Deku})                 # save old lady, need sword; TIME: Night 1
check(M.KafeiMask,       S.EastClockTown,         {M.Deku})                 # talk to Madame Aroma
check(M.Bremen,          S.LaundryPool,           {M.Deku})                 # Guru-Guru; TIME: night
check(M.Kamaro,          S.TerminaField,          {Songs.Healing})           # Song of Healing on ghost; TIME: night
check(M.AllNight,        S.WestClockTown,         {M.Blast})                # Curiosity Shop; TIME: Night 3, 500 rupees
check(I.AdultWallet,     S.WestClockTown)                                   # 200 rupees in bank
check(I.BombersNotebook, S.EastClockTown,         {M.Deku, I.Magic})         # be human, pop balloon
check(I.MoonsTear,       S.Observatory,           {I.Magic})                 # look through telescope (need Bombers' code)
check(I.RoomKey,         S.EastClockTown,         {M.Deku})                  # Anju at Stock Pot Inn, not Deku

# =====================
# === SONG OF SOARING
# =====================
check(Songs.Soaring,     S.SouthernSwamp,         {I.Ocarina})

# =====================
# === BOTTLES
# =====================
check(I.Bottle,          S.SouthernSwamp,         {M.Deku})                 # Kotake/Koume, need human form
check(I.BottleAliens,    S.RomaniRanch,           {I.Bow, I.Epona})         # TIME: Night 1, by 3 AM
check(I.GoldDust,        S.GoronRacetrack,        {M.Goron, R.Goht})
check(I.BottleGoldDust,  S.WestClockTown,         {I.GoldDust})             # sell at Curiosity Shop; TIME: any night after 10 PM
check(I.BottleGraveyard, S.IkanaGraveyard,       {I.Bow, M.Captain})        # TIME: Night 3
check(I.BottleBeaver,    S.ZoraCape,             {M.Zora, I.Hookshot})      # beaver race

# =====================
# === SOUTHERN SWAMP / WOODFALL
# =====================
check(I.MagicBeans,      S.DekuPalace)                                      # buy from bean seller
check(Songs.Sonata,      S.DekuPalace,            {M.Deku})
check(I.Bow,             S.WoodfallTemple,        {Songs.Sonata, M.Deku, I.Magic})
check(I.BossKeyWFT,      S.WoodfallTemple,        {I.Bow})
check(R.Odolwa,          S.WoodfallTemple,        {I.BossKeyWFT})
check(Songs.OathToOrder, S.WoodfallTemple,        {R.Odolwa})
check(M.Scents,          S.DekuPalace,            {R.Odolwa})               # Deku Butler race after Odolwa
check(M.Truth,           S.SwampSpiderHouse,      {M.Deku, I.Bow, I.BombBag})  # all 30 skulltulas
check(I.SpinAttack,      S.Woodfall,              {R.Odolwa})               # WF Great Fairy (15 stray fairies)

# =====================
# === MOUNTAIN / SNOWHEAD
# =====================
check(I.LensOfTruth,     S.LonePeakShrine,        {I.Magic, I.Bow, I.BombBag})
check(M.Goron,           S.MountainVillage,        {I.LensOfTruth, Songs.Healing})
check(M.DonGero,         S.MountainVillage,        {M.Goron})               # eat rock sirloin as Goron
check(Songs.LullabyIntro,S.GoronVillage,           {M.Goron})
check(Songs.Lullaby,     S.GoronShrine,            {Songs.LullabyIntro, M.Goron})
check(I.FireArrows,      S.SnowheadTemple,         {Songs.Lullaby, M.Goron, I.Magic})
check(I.BossKeySHT,      S.SnowheadTemple,         {I.FireArrows})
check(R.Goht,            S.SnowheadTemple,         {I.BossKeySHT})
check(I.DoubleMagic,     S.Snowhead,               {R.Goht})                # SH Great Fairy (15 stray fairies)

# === Swords (Mountain Village smithy) ===
check(I.RazorSword,      S.MountainVillage,        {I.FireArrows})          # fire arrows/HSW to thaw smithy
check(I.GildedSword,     S.MountainVillage,        {I.RazorSword, I.GoldDust})

# === Access items (post-Snowhead) ===
check(I.PowderKeg,       S.GoronVillage,           {M.Goron, I.FireArrows})
check(I.Epona,           S.RomaniRanch,            {I.PowderKeg})

# =====================
# === MILK ROAD / RANCH
# =====================
check(M.BunnyHood,       S.RomaniRanch,            {M.Bremen, I.Epona})     # march chicks with Bremen
check(M.Romani,          S.RomaniRanch,            {I.BottleAliens})         # Cremia milk delivery; TIME: Night 2

# =====================
# === GREAT BAY
# =====================
check(M.Zora,            S.GreatBayCoast,          {Songs.Healing, I.Epona})
check(I.Hookshot,        S.PiratesFortress,        {M.Zora})
check(Songs.NewWave,     S.MarineResearchLab,      {M.Zora, I.Hookshot, I.Bottle, I.BottleAliens, I.BottleGoldDust})
check(I.IceArrows,       S.GreatBayTemple,         {Songs.NewWave, M.Zora})  # GBT dungeon item
check(I.BossKeyGBT,      S.GreatBayTemple,         {I.IceArrows})
check(R.Gyorg,           S.GreatBayTemple,         {I.BossKeyGBT})
check(I.EnhancedDefense, S.ZoraCape,               {R.Gyorg})               # GB Great Fairy (15 stray fairies)
check(I.GiantWallet,     S.OceanSpiderHouse,       {I.Epona})               # all skulltulas; TIME: Day 1

# =====================
# === IKANA / STONE TOWER
# =====================
check(M.Garo,            S.GormanTrack,            {I.Epona})               # TIME: Day 1 or 2
check(M.Stone,           S.IkanaTrail,             {I.LensOfTruth, I.Bottle})  # invisible soldier, need healing item
check(M.Captain,         S.IkanaGraveyard,         {Songs.Sonata, M.Garo, I.Hookshot})
check(Songs.Storms,      S.IkanaGraveyard,         {M.Captain})
check(M.Gibdo,           S.IkanaCanyon,            {Songs.Storms, Songs.Healing})
check(I.MirrorShield,    S.BeneathTheWell,         {M.Gibdo, I.BombBag, I.Bottle, I.MagicBeans, I.Epona})
check(Songs.Elegy,       S.IkanaCastle,            {I.MirrorShield, I.PowderKeg})
check(I.LightArrows,     S.StoneTowerTemple,       {Songs.Elegy, M.Goron, M.Zora, M.Deku})
check(M.Giant,           S.StoneTowerTemple,       {I.LightArrows})          # STT dungeon item
check(I.BossKeySTT,      S.StoneTowerTemple,       {I.LightArrows})
check(R.Twinmold,        S.StoneTowerTemple,       {I.BossKeySTT, M.Giant})
check(I.GreatFairySword, S.IkanaCanyon,            {R.Twinmold})            # Ikana Great Fairy (15 stray fairies)

# =====================
# === MILK BAR / MULTI-REGION
# =====================
check(M.CircusLeader,    S.EastClockTown,          {M.Romani, M.Deku, M.Goron, M.Zora, I.Ocarina})

# =====================
# === MOON
# =====================
check(E.EnterMoon,       S.ClockTowerRooftop,
      {R.Odolwa, R.Goht, R.Gyorg, R.Twinmold, Songs.OathToOrder, Songs.Soaring})
check(E.KillMajora,      S.TheMoon,               {E.EnterMoon})

# =====================
# === UPGRADES
# =====================
# Bomb Bag 30: bomb shop if you saved old lady, or curiosity shop if you didn't
check(I.BombBag30,       S.WestClockTown,          {I.BombBag, M.Blast})    # bomb shop after saving old lady
# Bomb Bag 40: mountain scrub as Goron, or swamp scrub as human with swamp deed
check(I.BombBag40,       S.MountainVillage,        {I.BombBag30, M.Goron})  # TODO: OR swamp deed path
# Quivers: progressive, whichever archery you do first gives 40, second gives 50
check(I.Quiver40,        S.EastClockTown,          {I.Bow})                 # town shooting gallery
check(I.Quiver50,        S.SouthernSwamp,          {I.Bow, I.Quiver40})     # road to southern swamp shooting gallery

# =====================
# === KAFEI QUEST
# =====================
# Step 0: Kafei's Mask from Madame Aroma (already defined above as M.KafeiMask)
# Step 1-2: Wear Kafei's Mask, talk to Anju, midnight meeting Night 1 -> Letter to Kafei
check(I.LetterToKafei,    S.EastClockTown,    {M.KafeiMask, I.RoomKey})     # TIME: Night 1 midnight
# Step 3-4: Mail letter, find Kafei in hideout Day 2 -> Pendant of Memories
check(I.PendantOfMemories,S.LaundryPool,      {I.LetterToKafei})            # TIME: Day 2
# Step 5-6: Give pendant to Anju, then Day 3 go to hideout -> Priority Mail + Keaton Mask
check(I.PriorityMail,    S.LaundryPool,       {I.PendantOfMemories})        # TIME: Day 3
check(M.Keaton,           S.LaundryPool,       {I.PendantOfMemories})        # same event as Priority Mail
# Step 7 (EXCLUSIVE per cycle - can only do one per quest run):
check(M.Postman,          S.WestClockTown,     {I.PriorityMail})             # give to Postman at Post Office
check(I.BottleMadameAroma,S.EastClockTown,     {I.PriorityMail, M.Romani})  # give to Madame Aroma in Milk Bar
# Step 8-9: Help Kafei at Sakon's Hideout (Ikana), return to CT -> Couple's Mask
check(M.Couple,           S.EastClockTown,
      {I.PendantOfMemories, M.Garo, I.Hookshot})                            # TIME: Night 3, ~1:30-2:30 AM

# =====================
# === FIERCE DEITY
# =====================
# All 20 non-transformation masks given to Moon children
check(M.FierceDeity,      S.TheMoon,
      {M.GreatFairy, M.Blast, M.Stone, M.Bremen, M.Kamaro, M.KafeiMask,
       M.AllNight, M.BunnyHood, M.DonGero, M.Scents, M.Truth,
       M.Captain, M.Garo, M.Gibdo, M.Romani, M.CircusLeader, M.Giant,
       M.Keaton, M.Postman, M.Couple, E.EnterMoon})

# TODO: Heart Pieces (52)


# === Goal sets ===
ANY_PERCENT_GOALS = [E.KillMajora]
ALL_MASKS_GOALS = [E.KillMajora]  # TODO: add all mask checks when Kafei quest is done
