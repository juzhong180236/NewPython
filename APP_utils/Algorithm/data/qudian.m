%������뻻���Ժ����Ļ����͸�һ��designspace�Ͳ��Ժ��������־���
designspace = [0 0;1 1];  %������
ndv = size(designspace,2);
ntrain=10*ndv;    %ѵ�������
ntest = 1000*ndv; %���Ե����
xtrain = lhsdesign(ntrain,ndv);   
xtrain = xtrain.*repmat(designspace(2,:)-designspace(1,:),[ntrain,1])+repmat(designspace(1,:),[ntrain,1]);
ytrain = test7fun(xtrain);    %���Ժ���hart3
xtest=lhsdesign(ntest,ndv); 
xtest=xtest.*repmat(designspace(2,:)-designspace(1,:),[ntest,1])+repmat(designspace(1,:),[ntest,1]);
ytest = test7fun(xtest);  %���Ժ���hart3
xlswrite('C:\Users\asus\Desktop\1.xlsx',xtrain,'Sheet1','A1')
xlswrite('C:\Users\asus\Desktop\1.xlsx',ytrain,'Sheet1','E1')
xlswrite('C:\Users\asus\Desktop\1.xlsx',xtest,'Sheet2','A1')
xlswrite('C:\Users\asus\Desktop\1.xlsx',ytest,'Sheet2','E1')