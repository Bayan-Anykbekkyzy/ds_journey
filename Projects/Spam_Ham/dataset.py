import numpy as np
import re

class Dataset:
    def __init__(self, X, y):
        self._x = X # сообщения 
        self._y = y # метки ["spam", "ham"]
        self.train = None # кортеж из (X_train, y_train)
        self.val = None # кортеж из (X_val, y_val)
        self.test = None # кортеж из (X_test, y_test)
        self.label2num = {} # словарь, используемый для преобразования меток в числа
        self.num2label = {} # словарь, используемый для преобразования числа в метки
        self._transform()
        
    def __len__(self):
        return len(self._x)
    
    def _transform(self):
        '''
        Функция очистки сообщения и преобразования меток в числа.
        '''
        # Начало вашего кода
        accepted=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0']
        
        for idx, el in enumerate(np.unique(self._y)):
            self.num2label[idx] = el
            self.label2num[el] = idx
            self._y[self._y==el]=idx
        
        self._x=np.array([x.lower() for x in self._x])
        rmv_el=np.unique([self._x[i][j] for i in range(len(self._x)) for j in range(len(self._x[i])) if self._x[i][j] not in accepted])
        for elem in rmv_el:
            self._x=np.char.replace(self._x, elem, ' ')
        for idx in range(len(self._x)):
            self._x[idx]=" ".join(np.char.split(self._x[idx]).item())
        # Конец вашего кода
        pass

    def split_dataset(self, val=0.1, test=0.1):
        '''
        Функция, которая разбивает набор данных на наборы train-validation-test.
        '''
        # Начало вашего кода
        np.random.seed(1)
        indices=np.arange(0,len(self._x))
        np.random.shuffle(indices)
        
        val_indices=indices[:round(val*len(self._x))]
        test_indices=indices[round(val*len(self._x)):round((val+test)*len(self._x))]
        train_indices=indices[round((val+test)*len(self._x)):]
        
        self.train=self._x[train_indices],self._y[train_indices]
        self.val=self._x[val_indices],self._y[val_indices]
        self.test=self._x[test_indices],self._y[test_indices]
        # Конец вашего кода
        pass