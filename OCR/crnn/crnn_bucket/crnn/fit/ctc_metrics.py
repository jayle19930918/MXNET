from __future__ import print_function
import pdb
import numpy as np


class CtcMetrics(object):
    def __init__(self,):
        pass

    @staticmethod
    def ctc_label(p):
        """
        Iterates through p, identifying non-zero and non-repeating values, and returns them in a list
        Parameters
        ----------
        p: list of int

        Returns
        -------
        list of int
        """
        ret = []
        p1 = [0] + p
        for i, _ in enumerate(p):
            c1 = p1[i]
            c2 = p1[i+1]
            if c2 == 0 or c2 == c1:
                continue
            ret.append(c2)
        return ret

    @staticmethod
    def _remove_blank(l):
        """ Removes trailing zeros in the list of integers and returns a new list of integers"""
        ret = []
        for i, _ in enumerate(l):
            if l[i] == 0:
                break
            ret.append(l[i])
        return ret

    @staticmethod
    def _lcs(p, l):
        """ Calculates the Longest Common Subsequence between p and l (both list of int) and returns its length"""
        # Dynamic Programming Finding LCS
        if len(p) == 0:
            return 0
        P = np.array(list(p)).reshape((1, len(p)))
        L = np.array(list(l)).reshape((len(l), 1))
        M = np.int32(P == L)
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                up = 0 if i == 0 else M[i-1, j]
                left = 0 if j == 0 else M[i, j-1]
                M[i, j] = max(up, left, M[i, j] if (i == 0 or j == 0) else M[i, j] + M[i-1, j-1])
        return M.max()

    def accuracy(self, label, pred):
        """ Simple accuracy measure: number of 100% accurate predictions divided by total number """
        hit = 0.
        total = 0.
        batch_size = label.shape[0]
        #pdb.set_trace()
        seq_len = pred.shape[0]//128
        for i in range(batch_size):
            l = self._remove_blank(label[i])
            p = []
            for k in range(seq_len):
                p.append(np.argmax(pred[k * batch_size + i]))
            p = self.ctc_label(p)
            if len(p) == len(l):
                match = True
                for k, _ in enumerate(p):
                    if p[k] != int(l[k]):
                        match = False
                        break
                if match:
                    hit += 1.0
            total += 1.0
        assert total == batch_size
        return hit / total


