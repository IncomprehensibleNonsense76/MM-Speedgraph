"""Bombers Notebook quests — multi-scene, multi-cycle quest chains.

Quest checks are registered on the scene nodes where they happen,
but the quest modules here define the logical flow and can add
cross-scene dependencies or cycle constraints.

Quests are repeatable across cycles. Some require multiple runs
(e.g., Kafei quest for both Postman's Hat AND Madame Aroma Bottle).
"""
