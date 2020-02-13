%Uppg. 1
p = [1 4 -84 -304 1280 3072];
roots(p)
polyval(p,8)
polyval(p,-6)
%% uppg. 2
g = poly([-5, -4, 2, 6]);
h = linspace (-50, 50, 10000);
plot(h, polyval(g,h))
axis([-100 100 -10 50])
%% uppg. 3
fun = @(x) 2.*(x.^3) + 3.*sin(2.*x)
%%
q = integral(fun, 1.2, 2.7)
plot(h,fun(h))
%% uppg. 4
u = @(x) cos(exp(x))./(1-x);
fplot(u,[2 3])
grid on
[x,y] = fminbnd(u,2,3)
%% uppg 5
v = @(x) exp(-x.^2) - 9.*x.^2 + x;
v2= @(x) -v(x)
plot(h,v2(h))
grid on
fminbnd(v2, -5, 5)
v(0.05)
%%
fsolve(v, [-0.25, 0.4])
%% uppg 6
help diag
%%
A = 5*diag(ones(9,1),1) + 5*diag(ones(9,1),-1) + 2*eye(10)
det(A)
%%
help repmat
%% uppg 7
m = complexmat1(5, -2+i, 1-i)
%% uppg 8
z = 0.5 + 0.5*i
%%
z = z * z
z = z * z
%% uppg 9
converge11(0.5+0.5i)
%%
converge11(1.1)
%% Uppg. 10
m = complexmat1(5, -2+i, 1-i)
%%
v = arrayfun(@converge11, m)
%%
image(v)
%% Uppg. 11
b = complexmat1(1000, -2+i, 1-i)
%%
a = arrayfun(@converge11, b)
%%
%image(a)
%%
%c = arrayfun(@converge22, b)
