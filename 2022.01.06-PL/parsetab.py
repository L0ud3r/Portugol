
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "left+-left*/rightuminusleftorxorleftandand assign ate de escreva faca false fimfuncao fimpara funcao leia not nr or para string true var vartype xor code : s  code : code ';' s  ciclo : para var de e ate e faca com_list ';' fimpara  func : funcao var '(' args ')' com_list ';' fimfuncao  comando : e\n                    | ciclo  comando : var assign e  comando : escreva '(' e_list ')'  comando : leia '(' var_list ')'  comando : vartype ':' var_list  s : func\n              | comando  e_list : e\n                   | e_list ',' e  n : nr\n              | '-' e  %prec uminus   n : e '+' e\n              | e '-' e\n              | e '*' e\n              | e '/' e  b : f\n              | e or e\n              | e and e\n              | e xor e  f : true  f : false  f : not f  e : var  e : '(' e ')'  e : b\n              | n\n              | string  e : var '(' e_list ')'\n              | var '(' ')'  com_list : comando\n                     | com_list ';' comando  var_list : var\n                     | var_list ',' var  args :\n                 | var_list "
    
_lr_action_items = {'funcao':([0,23,],[5,5,]),'var':([0,5,7,16,19,23,25,26,29,30,31,32,33,34,35,36,37,38,43,60,64,67,69,72,76,77,81,],[6,24,28,39,28,6,28,28,28,28,28,28,28,28,28,28,58,58,58,28,28,71,6,28,6,6,6,]),'escreva':([0,23,69,76,77,81,],[10,10,10,10,10,10,]),'leia':([0,23,69,76,77,81,],[11,11,11,11,11,11,]),'vartype':([0,23,69,76,77,81,],[12,12,12,12,12,12,]),'(':([0,6,7,10,11,19,23,24,25,26,28,29,30,31,32,33,34,35,36,60,64,69,72,76,77,81,],[7,26,7,36,37,7,7,43,7,7,26,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,]),'string':([0,7,19,23,25,26,29,30,31,32,33,34,35,36,60,64,69,72,76,77,81,],[15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,]),'para':([0,23,69,76,77,81,],[16,16,16,16,16,16,]),'nr':([0,7,19,23,25,26,29,30,31,32,33,34,35,36,60,64,69,72,76,77,81,],[18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,]),'-':([0,6,7,8,13,14,15,17,18,19,20,21,23,25,26,27,28,29,30,31,32,33,34,35,36,40,41,44,46,47,48,49,50,51,52,53,54,55,60,63,64,68,69,70,72,75,76,77,81,],[19,-28,19,33,-30,-31,-32,-21,-15,19,-25,-26,19,19,19,33,-28,19,19,19,19,19,19,19,19,-16,-27,33,-34,33,-29,-22,-23,-24,-17,-18,-19,-20,19,-33,19,33,19,33,19,33,19,19,19,]),'true':([0,7,19,22,23,25,26,29,30,31,32,33,34,35,36,60,64,69,72,76,77,81,],[20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,]),'false':([0,7,19,22,23,25,26,29,30,31,32,33,34,35,36,60,64,69,72,76,77,81,],[21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,]),'not':([0,7,19,22,23,25,26,29,30,31,32,33,34,35,36,60,64,69,72,76,77,81,],[22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,]),'$end':([1,2,3,4,6,8,9,13,14,15,17,18,20,21,28,40,41,42,44,46,48,49,50,51,52,53,54,55,58,59,63,65,66,71,78,82,],[0,-1,-11,-12,-28,-5,-6,-30,-31,-32,-21,-15,-25,-26,-28,-16,-27,-2,-7,-34,-29,-22,-23,-24,-17,-18,-19,-20,-37,-10,-33,-8,-9,-38,-4,-3,]),';':([1,2,3,4,6,8,9,13,14,15,17,18,20,21,28,40,41,42,44,46,48,49,50,51,52,53,54,55,58,59,63,65,66,71,73,74,78,79,80,82,],[23,-1,-11,-12,-28,-5,-6,-30,-31,-32,-21,-15,-25,-26,-28,-16,-27,-2,-7,-34,-29,-22,-23,-24,-17,-18,-19,-20,-37,-10,-33,-8,-9,-38,76,-35,-4,-36,81,-3,]),'assign':([6,],[25,]),'or':([6,8,13,14,15,17,18,20,21,27,28,40,41,44,46,47,48,49,50,51,52,53,54,55,63,68,70,75,],[-28,29,-30,-31,-32,-21,-15,-25,-26,29,-28,29,-27,29,-34,29,-29,-22,-23,-24,29,29,29,29,-33,29,29,29,]),'and':([6,8,13,14,15,17,18,20,21,27,28,40,41,44,46,47,48,49,50,51,52,53,54,55,63,68,70,75,],[-28,30,-30,-31,-32,-21,-15,-25,-26,30,-28,30,-27,30,-34,30,-29,30,-23,30,30,30,30,30,-33,30,30,30,]),'xor':([6,8,13,14,15,17,18,20,21,27,28,40,41,44,46,47,48,49,50,51,52,53,54,55,63,68,70,75,],[-28,31,-30,-31,-32,-21,-15,-25,-26,31,-28,31,-27,31,-34,31,-29,-22,-23,-24,31,31,31,31,-33,31,31,31,]),'+':([6,8,13,14,15,17,18,20,21,27,28,40,41,44,46,47,48,49,50,51,52,53,54,55,63,68,70,75,],[-28,32,-30,-31,-32,-21,-15,-25,-26,32,-28,-16,-27,32,-34,32,-29,-22,-23,-24,-17,-18,-19,-20,-33,32,32,32,]),'*':([6,8,13,14,15,17,18,20,21,27,28,40,41,44,46,47,48,49,50,51,52,53,54,55,63,68,70,75,],[-28,34,-30,-31,-32,-21,-15,-25,-26,34,-28,-16,-27,34,-34,34,-29,-22,-23,-24,34,34,-19,-20,-33,34,34,34,]),'/':([6,8,13,14,15,17,18,20,21,27,28,40,41,44,46,47,48,49,50,51,52,53,54,55,63,68,70,75,],[-28,35,-30,-31,-32,-21,-15,-25,-26,35,-28,-16,-27,35,-34,35,-29,-22,-23,-24,35,35,-19,-20,-33,35,35,35,]),':':([12,],[38,]),')':([13,14,15,17,18,20,21,26,27,28,40,41,43,45,46,47,48,49,50,51,52,53,54,55,56,57,58,61,62,63,70,71,],[-30,-31,-32,-21,-15,-25,-26,46,48,-28,-16,-27,-39,63,-34,-13,-29,-22,-23,-24,-17,-18,-19,-20,65,66,-37,69,-40,-33,-14,-38,]),',':([13,14,15,17,18,20,21,28,40,41,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,62,63,70,71,],[-30,-31,-32,-21,-15,-25,-26,-28,-16,-27,64,-34,-13,-29,-22,-23,-24,-17,-18,-19,-20,64,67,-37,67,67,-33,-14,-38,]),'ate':([13,14,15,17,18,20,21,28,40,41,46,48,49,50,51,52,53,54,55,63,68,],[-30,-31,-32,-21,-15,-25,-26,-28,-16,-27,-34,-29,-22,-23,-24,-17,-18,-19,-20,-33,72,]),'faca':([13,14,15,17,18,20,21,28,40,41,46,48,49,50,51,52,53,54,55,63,75,],[-30,-31,-32,-21,-15,-25,-26,-28,-16,-27,-34,-29,-22,-23,-24,-17,-18,-19,-20,-33,77,]),'de':([39,],[60,]),'fimfuncao':([76,],[78,]),'fimpara':([81,],[82,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'code':([0,],[1,]),'s':([0,23,],[2,42,]),'func':([0,23,],[3,3,]),'comando':([0,23,69,76,77,81,],[4,4,74,79,74,79,]),'e':([0,7,19,23,25,26,29,30,31,32,33,34,35,36,60,64,69,72,76,77,81,],[8,27,40,8,44,47,49,50,51,52,53,54,55,47,68,70,8,75,8,8,8,]),'ciclo':([0,23,69,76,77,81,],[9,9,9,9,9,9,]),'b':([0,7,19,23,25,26,29,30,31,32,33,34,35,36,60,64,69,72,76,77,81,],[13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,]),'n':([0,7,19,23,25,26,29,30,31,32,33,34,35,36,60,64,69,72,76,77,81,],[14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,]),'f':([0,7,19,22,23,25,26,29,30,31,32,33,34,35,36,60,64,69,72,76,77,81,],[17,17,17,41,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,]),'e_list':([26,36,],[45,56,]),'var_list':([37,38,43,],[57,59,62,]),'args':([43,],[61,]),'com_list':([69,77,],[73,80,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> code","S'",1,None,None,None),
  ('code -> s','code',1,'p_code1','logic_grammar.py',25),
  ('code -> code ; s','code',3,'p_code2','logic_grammar.py',29),
  ('ciclo -> para var de e ate e faca com_list ; fimpara','ciclo',10,'p_ciclo','logic_grammar.py',44),
  ('func -> funcao var ( args ) com_list ; fimfuncao','func',8,'p_func','logic_grammar.py',62),
  ('comando -> e','comando',1,'p_comando1','logic_grammar.py',71),
  ('comando -> ciclo','comando',1,'p_comando1','logic_grammar.py',72),
  ('comando -> var assign e','comando',3,'p_comando2','logic_grammar.py',76),
  ('comando -> escreva ( e_list )','comando',4,'p_comando3','logic_grammar.py',87),
  ('comando -> leia ( var_list )','comando',4,'p_comando4','logic_grammar.py',98),
  ('comando -> vartype : var_list','comando',3,'p_comando5','logic_grammar.py',102),
  ('s -> func','s',1,'p_s','logic_grammar.py',110),
  ('s -> comando','s',1,'p_s','logic_grammar.py',111),
  ('e_list -> e','e_list',1,'p_e_list','logic_grammar.py',117),
  ('e_list -> e_list , e','e_list',3,'p_e_list','logic_grammar.py',118),
  ('n -> nr','n',1,'p_n1','logic_grammar.py',126),
  ('n -> - e','n',2,'p_n1','logic_grammar.py',127),
  ('n -> e + e','n',3,'p_n2','logic_grammar.py',131),
  ('n -> e - e','n',3,'p_n2','logic_grammar.py',132),
  ('n -> e * e','n',3,'p_n2','logic_grammar.py',133),
  ('n -> e / e','n',3,'p_n2','logic_grammar.py',134),
  ('b -> f','b',1,'p_b1','logic_grammar.py',140),
  ('b -> e or e','b',3,'p_b1','logic_grammar.py',141),
  ('b -> e and e','b',3,'p_b1','logic_grammar.py',142),
  ('b -> e xor e','b',3,'p_b1','logic_grammar.py',143),
  ('f -> true','f',1,'p_f1','logic_grammar.py',152),
  ('f -> false','f',1,'p_f2','logic_grammar.py',156),
  ('f -> not f','f',2,'p_f3','logic_grammar.py',160),
  ('e -> var','e',1,'p_e1','logic_grammar.py',166),
  ('e -> ( e )','e',3,'p_e2','logic_grammar.py',170),
  ('e -> b','e',1,'p_e3','logic_grammar.py',174),
  ('e -> n','e',1,'p_e3','logic_grammar.py',175),
  ('e -> string','e',1,'p_e3','logic_grammar.py',176),
  ('e -> var ( e_list )','e',4,'p_e4','logic_grammar.py',180),
  ('e -> var ( )','e',3,'p_e4','logic_grammar.py',181),
  ('com_list -> comando','com_list',1,'p_com_list','logic_grammar.py',189),
  ('com_list -> com_list ; comando','com_list',3,'p_com_list','logic_grammar.py',190),
  ('var_list -> var','var_list',1,'p_var_list','logic_grammar.py',200),
  ('var_list -> var_list , var','var_list',3,'p_var_list','logic_grammar.py',201),
  ('args -> <empty>','args',0,'p_args','logic_grammar.py',211),
  ('args -> var_list','args',1,'p_args','logic_grammar.py',212),
]
