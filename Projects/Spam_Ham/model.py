import numpy as np
import re

class Model:
    def __init__(self, alpha=1):
        self.vocab = set() # словарь, содержащий все уникальные слова из набора train
        self.spam = {} # словарь, содержащий частоту слов в спам-сообщениях из набора данных train.
        self.ham = {} # словарь, содержащий частоту слов в не спам-сообщениях из набора данных train.
        self.alpha = alpha # сглаживание
        self.label2num = None # словарь, используемый для преобразования меток в числа
        self.num2label = None # словарь, используемый для преобразования числа в метки
        self.Nvoc = None # общее количество уникальных слов в наборе данных train
        self.Nspam = None # общее количество уникальных слов в спам-сообщениях в наборе данных train
        self.Nham = None # общее количество уникальных слов в не спам-сообщениях в наборе данных train
        self._train_X, self._train_y = None, None
        self._val_X, self._val_y = None, None
        self._test_X, self._test_y = None, None
        
    def fit(self, dataset):
        '''
        dataset - объект класса Dataset
        Функция использует входной аргумент "dataset", 
        чтобы заполнить все атрибуты данного класса.
        '''
        # Начало вашего кода
        from dataset import Dataset
        
        for i in range(len(dataset.train[0])):
            for word in np.char.split(dataset.train[0][i]).item():
                self.vocab.update({word})    
        self.Nvoc=len(self.vocab)
        
        from collections import Counter                
        ham_words=[]
        spam_words=[]
        for i in range(len(dataset.train[0])):
            if dataset.train[1][i]==0:
                for word in np.char.split(dataset.train[0][i]).item():
                    ham_words.append(word)
            elif dataset.train[1][i]==1:
                for word in np.char.split(dataset.train[0][i]).item():
                    spam_words.append(word)
        self.ham=dict(Counter(ham_words))
        self.Nham=len(self.ham)
        self.spam=dict(Counter(spam_words))                
        self.Nspam=len(self.spam)                            
        
        self.label2num=dataset.label2num
        self.num2label=dataset.num2label
        self._train_X, self._train_y = dataset.train[0], dataset.train[1]
        self._val_X, self._val_y = dataset.val[0], dataset.val[1]
        self._test_X, self._test_y = dataset.test[0], dataset.test[1]
        # Конец вашего кода
        pass
    
    def inference(self, message):
        '''
        Функция принимает одно сообщение и, используя наивный байесовский алгоритм, определяет его как спам / не спам.
        '''
        # Начало вашего кода
        if type(message)!=np.str_:
            accepted=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0',' '] 
            message=message.lower()
            rmv_el=set([message[i][j] for i in range(len(message)) for j in range(len(message[i])) if message[i][j] not in accepted])
            for elem in rmv_el:
                message=message.replace(elem,'')
        
        from collections import Counter    
        ham_spam=dict(Counter(self._train_y))
        spam_res=ham_spam[1]/(ham_spam[0]+ham_spam[1])
        ham_res=ham_spam[0]/(ham_spam[0]+ham_spam[1])
        total_spams=0
        total_hams=0
        alpha=1
    
        # Total Hams
        for h_value in self.ham.values():
            total_hams+=h_value
        
        # Total Spams
        for s_value in self.spam.values():
            total_spams+=s_value   
    
        # Spam
        for word in message.split():
            if word in self.spam:
                spam_word=self.spam[word]
                spam_res*=((spam_word+alpha)/(total_spams+alpha*len(self.vocab)))
            elif word not in self.spam:
                spam_word=0
                spam_res*=((spam_word+alpha)/(total_spams+alpha*len(self.vocab)))
        
        # Ham
        for word in message.split():
            if word in self.ham:
                ham_word=self.ham[word]
                ham_res*=((ham_word+alpha)/(total_hams+alpha*len(self.vocab)))
            elif word not in self.ham:
                ham_word=0
                ham_res*=((ham_word+alpha)/(total_hams+alpha*len(self.vocab)))
        # Конец вашего кода
        if spam_res > ham_res:
            return "spam"
        return "ham"
    
    def validation(self):
        '''
        Функция предсказывает метки сообщений из набора данных validation,
        и возвращает точность предсказания меток сообщений.
        Вы должны использовать метод класса inference().
        '''
        # Начало вашего кода
        for idx in range(len(self._val_X)):
            p_condition=self.inference(self._val_X[idx])
            true_condition=self.num2label[self._val_y[idx]]
            
            if idx==0:
                accuracy=0
    
            if p_condition==true_condition:
                accuracy+=1
            
        val_acc=f"{accuracy/len(self._val_X)*100:.2f}%"
        # Конец вашего кода
        return val_acc 

    def test(self):
        '''
        Функция предсказывает метки сообщений из набора данных test,
        и возвращает точность предсказания меток сообщений.
        Вы должны использовать метод класса inference().
        '''
        # Начало вашего кода
        for idx in range(len(self._test_X)):
            p_condition=self.inference(self._test_X[idx])
            true_condition=self.num2label[self._test_y[idx]]
            
            if idx==0:
                accuracy=0
    
            if p_condition==true_condition:
                accuracy+=1
            
        test_acc=f"{accuracy/len(self._test_X)*100:.2f}%"
        # Конец вашего кода
        return test_acc