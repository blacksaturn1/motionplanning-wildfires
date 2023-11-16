

% x = ["Wumpus" "Firetruck"];
% y = [59.26 22.72];
% bar(x,y)

% Total time simulation: 74.80200000000018
% Total time wumpus: 63.16599999999991
% Total time firetruck: 20.26200000000003
% Total time simulation: 72.0809999999999
% Total time wumpus: 60.7249999999999
% Total time firetruck: 20.862000000000027
%3
% Total time simulation: 73.00599999999999
% Total time wumpus: 54.34199999999997
% Total time firetruck: 28.469000000000058
% 4
% Total time simulation: 72.56799999999997
% Total time wumpus: 52.27400000000005
% Total time firetruck: 29.974000000000128
% 5
% Total time simulation: 72.247
% Total time wumpus: 63.34699999999998
% Total time firetruck: 18.089000000000013

wumpus = 63.1659+60.7249+54.3419+52.274+63.34699
firetruck = 20.262+20.862+28.469+29.974+18.089
total = 19+20+18+22+19 
intact = 9+7+8+10+10
burned = 5+6+2+6+2
extinguished = 5+7+8+6+7

X = categorical({'Wumpus','Firetruck'});
y = [wumpus firetruck];
bar(X,y)

X = categorical({'intact','burned','extinguished'});
y = [intact/total burned/total extinguished/total];
bar(X,y)



