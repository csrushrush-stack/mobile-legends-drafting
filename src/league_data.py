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

# ---- MPL Philippines S18 - 131 games ---------------------------------------
PH18 = dict(id="ph", name="MPL Philippines S18", short="PH", region="Philippines",
            games=131, note="Current MPL PH season. Hirara is the most-picked hero in the league.",
            rows=[("Hirara",101,42,59,29),("Belerick",62,32,30,25),("Paquito",58,34,24,58),
                  ("Eudora",57,30,27,24),("Minotaur",49,22,27,20),("Nolan",45,30,15,25),
                  ("Gatotkaca",45,19,26,9),("Carmilla",44,22,22,35),("Valentina",40,19,21,23),
                  ("Barats",39,20,19,53),("Selena",35,17,18,58),("Uranus",34,18,16,60),
                  ("Claude",33,21,12,7),("Marcel",30,15,15,56),("Clint",30,21,9,10),
                  ("Obsidia",29,16,13,14),("Brody",28,7,21,19),("Zhuxin",27,16,11,22),
                  ("Rafaela",25,17,8,35),("Aulus",25,12,13,22),("Mathilda",24,11,13,34),
                  ("Melissa",23,10,13,52),("Atlas",22,13,9,107),("Novaria",21,10,11,11),
                  ("Suyou",21,11,10,5),("Gloo",20,13,7,35),("Esmeralda",20,7,13,28),
                  ("Moskov",20,7,13,10),("Hylos",20,10,10,3),("Miya",19,7,12,8),
                  ("Alice",16,7,9,15),("Freya",14,10,4,117),("Fanny",13,7,6,86),
                  ("Vexana",12,7,5,4),("Kimmy",12,6,6,3),("Ruby",11,7,4,11),("Harley",10,4,6,12),
                  ("Angela",10,4,6,10),("Badang",10,3,7,10),("Cici",10,4,6,5),("Chou",10,4,6,3),
                  ("Yi Sun-Shin",9,3,6,3),("Lylia",8,3,5,23),("Phoveus",8,3,5,3),
                  ("Lukas",7,4,3,6),("Cecilion",7,1,6,5),("Bruno",7,2,5,2),("Masha",6,5,1,40),
                  ("Kaja",6,4,2,11),("Kalea",6,3,3,8),("Karrie",6,3,3,0),("Dyrroth",5,3,2,4),
                  ("Sora",5,2,3,4),("Hanabi",4,3,1,8),("Hilda",4,3,1,5),("Hayabusa",4,1,3,2),
                  ("Beatrix",4,3,1,2),("Khufra",4,3,1,1),("Yve",3,3,0,2),("Arlott",3,2,1,1),
                  ("Pharsa",3,2,1,0),("Luo Yi",3,1,2,0),("Aurora",2,1,1,3),("Khaleed",2,1,1,1),
                  ("Harith",2,0,2,0),("Zetian",2,0,2,0),("Hanzo",1,0,1,1),("Fredrinn",1,0,1,1),
                  ("Saber",1,0,1,0),("Lolita",1,0,1,0),("Kagura",1,0,1,0),("Estes",1,1,0,0),
                  ("Lapu-lapu",1,1,0,0),("Leomord",1,0,1,0),("Lunox",1,1,0,0),("Granger",1,0,1,0),
                  ("Guinevere",1,0,1,0),("Ling",1,0,1,0),("Baxia",1,0,1,0),("Yu Zhong",1,0,1,0),
                  ("Edith",1,1,0,0),("Xavier",1,0,1,0)])

# ---- MPL Indonesia S18 - 153 games -----------------------------------------
ID18 = dict(id="id", name="MPL Indonesia S18", short="ID", region="Indonesia",
            games=153, note="Current MPL ID season, and the deepest hero pool of the three.",
            rows=[("Hirara",81,44,37,66),("Paquito",73,34,39,54),("Belerick",67,33,34,20),
                  ("Claude",59,31,28,10),("Uranus",49,23,26,49),("Eudora",45,26,19,25),
                  ("Selena",43,18,25,44),("Minotaur",42,18,24,28),("Nolan",41,24,17,38),
                  ("Atlas",38,22,16,106),("Barats",38,18,20,41),("Obsidia",38,23,15,23),
                  ("Valentina",38,14,24,20),("Rafaela",36,20,16,43),("Zhuxin",36,17,19,37),
                  ("Aulus",35,23,12,17),("Melissa",34,18,16,53),("Carmilla",34,21,13,50),
                  ("Gloo",32,20,12,36),("Moskov",32,17,15,14),("Freya",30,14,16,120),
                  ("Alice",28,15,13,13),("Brody",28,8,20,13),("Miya",27,17,10,18),
                  ("Cici",26,14,12,10),("Lylia",25,11,14,24),("Esmeralda",24,12,12,44),
                  ("Kimmy",23,12,11,7),("Mathilda",22,11,11,50),("Gatotkaca",21,11,10,7),
                  ("Fanny",20,10,10,89),("Marcel",20,12,8,80),("Novaria",20,10,10,38),
                  ("Harley",18,6,12,12),("Hylos",18,9,9,2),("Lukas",17,10,7,23),
                  ("Zetian",16,12,4,11),("Sora",15,6,9,7),("Suyou",15,5,10,1),
                  ("Yi Sun-shin",14,5,9,11),("Ruby",14,7,7,8),("Badang",14,8,6,7),
                  ("Chou",14,4,10,7),("Masha",13,4,9,40),("Cecilion",13,10,3,5),
                  ("Alpha",11,6,5,5),("Arlott",10,5,5,22),("Phoveus",10,5,5,16),("Chip",7,1,6,22),
                  ("Dyrroth",7,3,4,1),("Clint",7,3,4,0),("Pharsa",6,2,4,0),("Hayabusa",5,2,3,2),
                  ("Kalea",5,1,4,1),("Terizla",5,3,2,0),("Hanabi",4,2,2,3),("Hanzo",4,2,2,3),
                  ("Lunox",4,0,4,1),("Yve",4,3,1,0),("Kaja",3,1,2,10),("Guinevere",3,2,1,6),
                  ("Angela",3,0,3,3),("Saber",3,2,1,2),("Fredrinn",3,1,2,2),("Hilda",3,3,0,0),
                  ("Vexana",2,1,1,5),("Bruno",2,1,1,1),("Estes",2,1,1,1),("Faramis",2,1,1,0),
                  ("Khaleed",2,1,1,0),("Leomord",2,1,1,0),("Valir",2,1,1,0),("Harith",2,0,2,0),
                  ("Kadita",2,0,2,0),("Karrie",2,0,2,0),("Odette",2,0,2,0),("Ling",1,0,1,1),
                  ("Ixia",1,1,0,0),("Kagura",1,1,0,0),("Lapu-Lapu",1,1,0,0),("Wanwan",1,1,0,0),
                  ("Argus",1,0,1,0),("Edith",1,0,1,0),("Granger",1,0,1,0),("Joy",1,0,1,0),
                  ("Khufra",1,0,1,0),("Lesley",1,0,1,0),("Luo Yi",1,0,1,0),("Minsitthar",1,0,1,0),
                  ("Tigreal",1,0,1,0),("Yu Zhong",1,0,1,0)])

# ---- MSL Myanmar S4 - 109 games --------------------------------------------
MM4 = dict(id="mm", name="MSL Myanmar S4", short="MM", region="Myanmar",
            games=109, note="Myanmar won Asian Games gold off the back of this league.",
            rows=[("Hirara",75,34,41,32),("Paquito",63,35,28,21),("Eudora",60,34,26,16),
                  ("Belerick",59,30,29,40),("Uranus",43,23,20,54),("Gloo",38,23,15,31),
                  ("Zhuxin",34,15,19,28),("Barats",31,12,19,26),("Minotaur",31,18,13,22),
                  ("Obsidia",29,12,17,15),("Nolan",29,17,12,10),("Rafaela",26,13,13,24),
                  ("Carmilla",25,9,16,35),("Brody",24,19,5,30),("Esmeralda",24,10,14,21),
                  ("Miya",24,12,12,7),("Gatotkaca",23,12,11,9),("Selena",22,11,11,24),
                  ("Melissa",21,13,8,44),("Freya",18,12,6,90),("Moskov",18,5,13,18),
                  ("Yi Sun-shin",17,8,9,14),("Dyrroth",17,11,6,12),("Alice",17,9,8,8),
                  ("Novaria",17,8,9,7),("Aulus",15,5,10,10),("Chou",15,4,11,5),("Clint",14,7,7,3),
                  ("Sora",13,6,7,6),("Granger",13,7,6,3),("Ruby",12,5,7,8),("Claude",12,6,6,5),
                  ("Kimmy",12,7,5,3),("Hylos",11,4,7,3),("Zetian",11,6,5,1),("Atlas",10,4,6,97),
                  ("Fanny",10,6,4,34),("Marcel",9,5,4,87),("Lylia",9,5,4,12),("Suyou",9,3,6,8),
                  ("Valentina",8,4,4,27),("Mathilda",8,5,3,13),("Cici",8,2,6,9),
                  ("Phoveus",8,4,4,5),("Bruno",8,4,4,4),("Kaja",7,3,4,11),("Vexana",7,1,6,2),
                  ("Masha",5,3,2,20),("Arlott",5,4,1,2),("Cecilion",5,2,3,2),("Lukas",5,2,3,2),
                  ("Harley",4,3,1,10),("Kalea",4,2,2,5),("Guinevere",4,3,1,4),("Angela",4,1,3,3),
                  ("Leomord",4,2,2,1),("Aurora",4,2,2,0),("Khaleed",3,2,1,2),("Hanabi",3,0,3,2),
                  ("Harith",3,1,2,1),("Gord",3,2,1,0),("Tigreal",2,0,2,1),("Yu Zhong",2,1,1,0),
                  ("Beatrix",2,0,2,0),("Chip",1,1,0,12),("Badang",1,1,0,2),("Ixia",1,1,0,2),
                  ("Odette",1,0,1,2),("Valir",1,1,0,1),("Kagura",1,0,1,1),("Faramis",1,1,0,0),
                  ("Jawhead",1,1,0,0),("Yve",1,1,0,0),("Argus",1,0,1,0),("Balmond",1,0,1,0),
                  ("Edith",1,0,1,0),("Karrie",1,0,1,0),("Pharsa",1,0,1,0)])

LEAGUES = [AG2026, PH18, ID18, MM4]
