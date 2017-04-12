mother(X,Y):-child(X,Y), woman(Y).
grandmother(X,Z):-child(X,Y),mother(Y,Z).
father(X,Y):-child(X,Y), man(Y).
grandfather(X,Z):-child(X,Y),father(Y,Z).
brother(X,Y):-mother(X,M), mother(Y,M),father(X,F), father(Y,F), X \= Y, man(Y).
sister(X,Y):-mother(X,M), mother(Y,M),father(X,F), father(Y,F), X \= Y, woman(Y).
bloodbrother(X,Y):-father(X,F), father(Y,F), mother(X,M), \+mother(Y,M), man(Y).
uterinebrother(X,Y):-mother(X,M),mother(Y,M), father(X,F), \+father(Y,F), man(Y).
bloodsister(X,Y):-father(X,F), father(Y,F), mother(X,M), \+mother(Y,M), woman(Y).
uterinesister(X,Y):-mother(X,M),mother(Y,M), father(X,F), \+father(Y,F), woman(Y).
cousinmother(X,Y):-mother(X,M), (sister(M,P); brother(M,P)), (mother(Y,P); father(Y,P)).
cousinfather(X,Y):-father(X,F), (sister(F,P); brother(F,P)), (mother(Y,P); father(Y,P)).
cousins(X,Y):-cousinfather(X,Y);cousinmother(X,Y), man(Y).
step(X,Y):-(bloodbrother(X,Z);bloodsister(X,Z)),(uterinebrother(Y,Z);uterinesister(Y,Z)).
ancestor(X,Y):-child(X,Y); ancestor(Y,Z).
man(vladimir).
man(geralt).
man(ivan).
man(kratos).
man(johan).
man(svyatopolk).
man(jerihon).
man(dwarf).
woman(troll).
woman(germes).
woman(ekaterina).
woman(lana).
woman(keytelin).
woman(elizaveta).
woman(vasilisa).
child(vladimir,ivan).
child(vladimir,ekaterina).
child(ekaterina,vasilisa).
child(ivan,elizaveta).
child(ivan,svyatopolk).
child(ekaterina,jerihon).
child(kratos,vasilisa).
child(kratos,jerihon).
child(geralt,ekaterina).
child(geralt,johan).
child(lana,ivan).
child(lana,svyatopolk).
child(germes,kratos).
child(dwarf,ivan).
child(dwarf,troll).
