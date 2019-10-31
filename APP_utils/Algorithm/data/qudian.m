%如果你想换测试函数的话，就改一下designspace和测试函数的名字就行
designspace = [0 0;1 1];  %定义域
ndv = size(designspace,2);
ntrain=10*ndv;    %训练点个数
ntest = 1000*ndv; %测试点个数
xtrain = lhsdesign(ntrain,ndv);   
xtrain = xtrain.*repmat(designspace(2,:)-designspace(1,:),[ntrain,1])+repmat(designspace(1,:),[ntrain,1]);
ytrain = test7fun(xtrain);    %测试函数hart3
xtest=lhsdesign(ntest,ndv); 
xtest=xtest.*repmat(designspace(2,:)-designspace(1,:),[ntest,1])+repmat(designspace(1,:),[ntest,1]);
ytest = test7fun(xtest);  %测试函数hart3
xlswrite('C:\Users\asus\Desktop\1.xlsx',xtrain,'Sheet1','A1')
xlswrite('C:\Users\asus\Desktop\1.xlsx',ytrain,'Sheet1','E1')
xlswrite('C:\Users\asus\Desktop\1.xlsx',xtest,'Sheet2','A1')
xlswrite('C:\Users\asus\Desktop\1.xlsx',ytest,'Sheet2','E1')