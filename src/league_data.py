# -*- coding: utf-8 -*-
"""League hero-stat tables for the draft app.

Every row is (hero, picks, wins, losses, bans).
Win/loss derived from the published win rate where the source gave a percentage.
'games' is the tournament game count, verified against the published ban% where possible.
"""

# ---- Asian Games 2026 (Aichi-Nagoya) - 32 games, 15 tracked heroes -------------
AG2026 = dict(id="ag", name="Asian Games 2026", short="AG26", region="International",
              games=32, note="MLBB's debut as an official medal event. Gold: Myanmar.",
              rows=[("Nolan",23,11,12,6),("Hirara",16,12,4,15),("Aulus",16,11,5,16),
                    ("Eudora",16,10,6,7),("Obsidia",15,9,6,6),("Esmeralda",14,7,7,8),
                    ("Atlas",13,8,5,19),("Minotaur",13,8,5,13),("Uranus",13,5,8,12),
                    ("Zhuxin",12,6,6,3),("Gloo",11,7,4,6),("Paquito",11,5,6,13),
                    ("Carmilla",11,3,8,19),("Belerick",9,2,7,4),("Valentina",6,6,0,6)])

# ---- MPL Philippines S18 - 128 games ---------------------------------------
PH18 = dict(id="ph", name="MPL Philippines S18", short="PH", region="Philippines",
            games=128, note="Current MPL PH season. Hirara is the most-picked hero in the league.",
            rows=[("Hirara",101,42,59,26),("Belerick",60,31,29,25),("Paquito",56,32,24,58),
                  ("Eudora",56,29,27,24),("Minotaur",48,22,26,20),("Nolan",45,30,15,22),
                  ("Carmilla",43,21,22,33),("Gatotkaca",42,18,24,9),("Valentina",40,19,21,22),
                  ("Barats",38,19,19,52),("Uranus",33,17,16,58),("Selena",33,16,17,58),
                  ("Claude",33,21,12,7),("Marcel",30,15,15,54),("Clint",30,21,9,10),
                  ("Brody",28,7,21,19),("Obsidia",28,15,13,13),("Zhuxin",26,15,11,21),
                  ("Rafaela",25,17,8,35),("Mathilda",24,11,13,34),("Melissa",23,10,13,52),
                  ("Atlas",22,13,9,104),("Aulus",22,10,12,22),("Novaria",21,10,11,11),
                  ("Gloo",20,13,7,34),("Moskov",20,7,13,10),("Suyou",20,11,9,5),
                  ("Hylos",20,10,10,3),("Esmeralda",19,7,12,27),("Miya",17,6,11,8),
                  ("Alice",16,7,9,14),("Freya",13,10,3,115),("Fanny",12,7,5,84),
                  ("Vexana",12,7,5,4),("Ruby",11,7,4,11),("Harley",10,4,6,12),
                  ("Angela",10,4,6,10),("Kimmy",10,6,4,3),("Badang",9,2,7,9),("Cici",9,4,5,5),
                  ("Chou",9,4,5,3),("Yi Sun-Shin",9,3,6,3),("Lylia",8,3,5,23),("Phoveus",8,3,5,3),
                  ("Lukas",7,4,3,6),("Cecilion",7,1,6,5),("Bruno",7,2,5,2),("Masha",6,5,1,37),
                  ("Kaja",6,4,2,11),("Kalea",6,3,3,8),("Karrie",6,3,3,0),("Dyrroth",5,3,2,4),
                  ("Sora",5,2,3,4),("Hanabi",4,3,1,8),("Hilda",4,3,1,5),("Hayabusa",4,1,3,2),
                  ("Beatrix",4,3,1,2),("Khufra",4,3,1,1),("Yve",3,3,0,2),("Arlott",3,2,1,1),
                  ("Pharsa",3,2,1,0),("Luo Yi",3,1,2,0),("Aurora",2,1,1,3),("Khaleed",2,1,1,1),
                  ("Harith",2,0,2,0),("Zetian",2,0,2,0),("Hanzo",1,0,1,1),("Fredrinn",1,0,1,1),
                  ("Saber",1,0,1,0),("Lolita",1,0,1,0),("Kagura",1,0,1,0),("Estes",1,1,0,0),
                  ("Lapu-lapu",1,1,0,0),("Leomord",1,0,1,0),("Lunox",1,1,0,0),("Granger",1,0,1,0),
                  ("Guinevere",1,0,1,0),("Ling",1,0,1,0),("Baxia",1,0,1,0),("Yu Zhong",1,0,1,0),
                  ("Edith",1,1,0,0),("Xavier",1,0,1,0)])

# ---- MPL Indonesia S18 - 146 games -----------------------------------------
ID18 = dict(id="id", name="MPL Indonesia S18", short="ID", region="Indonesia",
            games=146, note="Current MPL ID season, and the deepest hero pool of the three.",
            rows=[("Hirara",81,44,37,59),("Paquito",71,33,38,54),("Belerick",67,33,34,20),
                  ("Claude",59,31,28,10),("Uranus",48,23,25,48),("Eudora",44,26,18,24),
                  ("Selena",42,18,24,44),("Minotaur",42,18,24,26),("Nolan",38,21,17,34),
                  ("Obsidia",38,23,15,18),("Barats",37,17,20,41),("Valentina",36,13,23,19),
                  ("Rafaela",35,20,15,41),("Atlas",34,19,15,103),("Melissa",34,18,16,53),
                  ("Zhuxin",34,16,18,33),("Carmilla",32,20,12,45),("Gloo",31,19,12,36),
                  ("Moskov",31,17,14,13),("Aulus",30,22,8,15),("Brody",28,8,20,13),
                  ("Miya",27,17,10,17),("Alice",26,14,12,12),("Freya",24,10,14,119),
                  ("Lylia",24,11,13,24),("Esmeralda",22,12,10,41),("Mathilda",21,11,10,50),
                  ("Cici",21,11,10,8),("Gatotkaca",21,11,10,7),("Novaria",20,10,10,38),
                  ("Fanny",19,9,10,85),("Harley",18,6,12,12),("Kimmy",18,9,9,7),
                  ("Marcel",17,10,7,79),("Lukas",17,10,7,17),("Hylos",16,9,7,2),
                  ("Zetian",15,11,4,10),("Sora",15,6,9,7),("Yi Sun-shin",14,5,9,11),
                  ("Badang",14,8,6,7),("Chou",14,4,10,5),("Suyou",14,5,9,1),("Masha",13,4,9,33),
                  ("Ruby",13,6,7,8),("Cecilion",12,10,2,5),("Phoveus",9,4,5,15),
                  ("Arlott",8,4,4,21),("Alpha",8,4,4,4),("Chip",7,1,6,22),("Dyrroth",7,3,4,1),
                  ("Clint",7,3,4,0),("Pharsa",6,2,4,0),("Hayabusa",5,2,3,2),("Kalea",5,1,4,1),
                  ("Hanabi",4,2,2,3),("Hanzo",4,2,2,3),("Lunox",4,0,4,1),("Terizla",4,3,1,0),
                  ("Kaja",3,1,2,10),("Guinevere",3,2,1,6),("Angela",3,0,3,3),("Fredrinn",3,1,2,2),
                  ("Hilda",3,3,0,0),("Yve",3,2,1,0),("Vexana",2,1,1,5),("Saber",2,2,0,2),
                  ("Bruno",2,1,1,1),("Estes",2,1,1,1),("Faramis",2,1,1,0),("Khaleed",2,1,1,0),
                  ("Leomord",2,1,1,0),("Valir",2,1,1,0),("Harith",2,0,2,0),("Kadita",2,0,2,0),
                  ("Karrie",2,0,2,0),("Odette",2,0,2,0),("Ling",1,0,1,1),("Ixia",1,1,0,0),
                  ("Kagura",1,1,0,0),("Lapu-Lapu",1,1,0,0),("Argus",1,0,1,0),("Edith",1,0,1,0),
                  ("Granger",1,0,1,0),("Khufra",1,0,1,0),("Lesley",1,0,1,0),("Luo Yi",1,0,1,0),
                  ("Minsitthar",1,0,1,0),("Tigreal",1,0,1,0),("Yu Zhong",1,0,1,0)])

# ---- MSL Myanmar S4 - 104 games --------------------------------------------
MM4 = dict(id="mm", name="MSL Myanmar S4", short="MM", region="Myanmar",
            games=104, note="Myanmar won Asian Games gold off the back of this league.",
            rows=[("Hirara",71,32,39,31),("Paquito",61,34,27,21),("Eudora",59,34,25,16),
                  ("Belerick",55,27,28,39),("Uranus",42,22,20,51),("Gloo",37,23,14,31),
                  ("Zhuxin",32,14,18,25),("Barats",31,12,19,24),("Minotaur",29,17,12,21),
                  ("Obsidia",28,11,17,14),("Rafaela",26,13,13,23),("Carmilla",25,9,16,30),
                  ("Nolan",25,16,9,9),("Miya",24,12,12,7),("Brody",23,19,4,30),
                  ("Gatotkaca",23,12,11,8),("Selena",22,11,11,24),("Esmeralda",22,9,13,19),
                  ("Melissa",21,13,8,44),("Moskov",18,5,13,18),("Freya",17,11,6,86),
                  ("Yi Sun-shin",17,8,9,14),("Dyrroth",17,11,6,10),("Alice",15,8,7,7),
                  ("Novaria",14,7,7,7),("Chou",14,3,11,4),("Clint",14,7,7,3),("Granger",13,7,6,3),
                  ("Ruby",12,5,7,8),("Aulus",12,3,9,8),("Claude",12,6,6,4),("Sora",12,5,7,4),
                  ("Kimmy",11,7,4,3),("Hylos",11,4,7,3),("Fanny",10,6,4,34),("Atlas",9,4,5,93),
                  ("Marcel",9,5,4,84),("Lylia",9,5,4,12),("Zetian",9,5,4,1),("Mathilda",8,5,3,13),
                  ("Suyou",8,2,6,8),("Phoveus",8,4,4,5),("Valentina",7,3,4,27),("Kaja",7,3,4,11),
                  ("Cici",7,2,5,7),("Vexana",7,1,6,2),("Bruno",6,3,3,4),("Cecilion",5,2,3,2),
                  ("Masha",4,3,1,16),("Harley",4,3,1,10),("Kalea",4,2,2,5),("Guinevere",4,3,1,4),
                  ("Lukas",4,2,2,2),("Angela",4,1,3,2),("Leomord",4,2,2,1),("Aurora",4,2,2,0),
                  ("Arlott",3,3,0,2),("Hanabi",3,0,3,2),("Khaleed",3,2,1,1),("Harith",3,1,2,1),
                  ("Gord",3,2,1,0),("Tigreal",2,0,2,1),("Yu Zhong",2,1,1,0),("Beatrix",2,0,2,0),
                  ("Chip",1,1,0,12),("Badang",1,1,0,2),("Ixia",1,1,0,2),("Odette",1,0,1,2),
                  ("Valir",1,1,0,1),("Kagura",1,0,1,1),("Jawhead",1,1,0,0),("Yve",1,1,0,0),
                  ("Argus",1,0,1,0),("Balmond",1,0,1,0),("Edith",1,0,1,0),("Karrie",1,0,1,0),
                  ("Pharsa",1,0,1,0)])

LEAGUES = [AG2026, PH18, ID18, MM4]
