#!/bin/env python
#-*- encoding: utf-8 -*-


import sys
import time
import math
import codecs
import pandas as pd
import numpy as np
from numpy import log, min


def _profiling(func):
    def wrapper(obj, *args, **argv):
        s = time.time()
        ret = func(obj, *args, **argv)
        e = time.time()
        print('func=%s, run_time=%.6fms' % (func.func_name,
            (e-s)*1000))
        return ret
    return wrapper


class Extractor(object):

    def __init__(self, max_ngrams = 5, min_freq = 10, min_support = 3,
                 entropy_threshold = 1.5):
        self._max_ngrams = max_ngrams
        self._min_freq = min_freq
        self._min_support = min_support
        self._min_entropy = entropy_threshold
        self._char_cnt = 0
        self._ngram_candidates_dict = {}
        self._pmi_candidates_dict = {}
        # NOTE: illegal char which should be dropped during preprocessing
        # you should adjust them according to corpus
        self._stopwords = set([u'\n', u'，', u'。', u'、', u'：', u'(',
            u')', u'[', u']', u'.', u',', u' ', u'\u3000', u'”', u'“',
            u'？', u'?', u'！', u'‘', u'’', u'…', '!', '+', '-', '*',
            '#', '"', "'", '^', ':', '/', '%', '=', ';', u'；', '@',
            '{', '}', u'」', u'「', u'．', u'—', u'－', u'『', u'』', 
            u'□', u'【', u'】', u'◆', u'（', u'）', u'·', u'`', u'·',
            u'\t', u'\\n'])


    def run(self, corpus_fpath, output_fpath):
        corpus = self._preprocess_corpus(corpus_fpath)
        self._pmi_candidates_dict = self._select_candidates_via_pmi(corpus)
        entropy_candidates = self._select_candidates_via_entropy(corpus)
        final_cand_dict = {}
        for n_size, pmi_cands in self._pmi_candidates_dict.items():
            entropy_cands = entropy_candidates[n_size]
            # NOTE: pmi_cands is superset of entropy_cands, thus its elmentes
            # can be accessed via entropy_cands.index here
            cands = pmi_cands[entropy_cands.index].sort_values(ascending=False)
            print(('n=%s, pmi_cand_size=%s, entropy_cand_size=%s'
                ', final_cand_size=%s') % (n_size, len(pmi_cands),
                len(entropy_cands), len(cands)))
            # concat pd.Series to collect (word, pmi, entropy, count) tuple
            ngram_counter = self._ngram_candidates_dict[n_size][cands.index]
            entropy_cands = entropy_cands[cands.index]
            res = pd.concat([cands, entropy_cands, ngram_counter], axis = 1,
                join_axes = [cands.index])
            out_fpath = '%s.%sgram' % (output_fpath, n_size)
            res.to_csv(out_fpath, encoding = 'utf-8', header = False)
            final_cand_dict[n_size] = res
        # summary: compute score of candidates
        sum_df = pd.concat(final_cand_dict.values())
        sum_df.columns = ['pmi', 'entropy', 'count']
        sum_df['score'] = (sum_df['pmi'] + sum_df['entropy']) * sum_df['count']
        sorted_result = sum_df.sort_values(by=['score'], ascending=False)
        sum_fpath = '%s.summary' % (output_fpath)
        sorted_result.to_csv(sum_fpath, encoding='utf-8', header=True)


    @_profiling
    def _preprocess_corpus(self, corpus_fpath):
        stopwords = self._stopwords 
        with codecs.open(corpus_fpath, 'r', 'utf-8') as rfd:
            corpus = rfd.read()
            for char in stopwords:
                corpus = corpus.replace(char, '')
        return corpus.lower()


    @_profiling
    def _select_candidates_via_pmi(self, corpus):
        word_candidates = {}
        for n_size in xrange(1, self._max_ngrams+1):
            ngrams = self._shingle_ngram_candidates(corpus, n_size)
            # stat ngram counter and filter low freq items
            counter = pd.Series(ngrams).value_counts()
            if 1 == n_size:
                self._char_cnt = counter.sum()
            counter = counter[counter >= self._min_freq]
            self._ngram_candidates_dict[n_size] = counter
            # filter via pmi
            dyn_counter = counter.copy()
            pmi_cache = []
            pmi_func = self._compute_pmi
            for k in xrange(n_size-1):
                left_seg_counter = self._ngram_candidates_dict[k+1]
                right_seg_counter = self._ngram_candidates_dict[n_size-k-1]
                pmi_vals = map(lambda w: pmi_func(counter[w],
                    left_seg_counter[w[:k+1]], right_seg_counter[w[k+1:]]),
                    dyn_counter.index)
                checked = np.array(pmi_vals) > self._min_support
                dyn_counter = dyn_counter[checked]
                pmi_vals = filter(lambda x: x > self._min_support, pmi_vals)
                pmi_cache.extend(zip(dyn_counter.index, pmi_vals))
            if n_size > 1:
                # select min pmi for the same word as its final pmi
                min_pmi_stats = pd.DataFrame(pmi_cache).groupby(0).min()
                word_candidates[n_size] = min_pmi_stats.loc[dyn_counter.index][1]
        return word_candidates


    @_profiling
    def _select_candidates_via_entropy(self, corpus):
        word_candidates = {}
        for n_size in xrange(2, self._max_ngrams+1):
            nearby_segs = self._shingle_ngram_candidates(corpus, n_size+2)
            nearby_segs = map(lambda x: (x[0], x[1:-1], x[-1]), nearby_segs)
            # NOTE: sort by word candidate can speed up computing entropy
            # Trie (e.g. pytrie) can also be used to speed up (and maybe faster)
            df = pd.DataFrame(nearby_segs).set_index(1).sort_index()
            pmi_candidates = self._pmi_candidates_dict[n_size]
            candidates = np.sort(np.intersect1d(pmi_candidates.index, df.index))
            func = self._compute_entropy
            s = time.time()
            left_entropy_vals = map(
                lambda w: func(pd.Series(df[0][w]).value_counts()), candidates)
            right_entropy_vals = map(
                lambda w: func(pd.Series(df[2][w]).value_counts()), candidates)
            e = time.time()
            print('n=%s, compute_entropy_time=%.6fms' % (n_size,
                (e-s)*1000))
            # select min(l_entropy, r_entropy) as final entropy for given word
            min_entropy_vals = map(lambda *args: min(args),
                zip(left_entropy_vals, right_entropy_vals))
            checked = np.array(min_entropy_vals) > self._min_entropy
            entropy_cands = pd.Series(min_entropy_vals, index = candidates)
            word_candidates[n_size] = entropy_cands[checked]
        return word_candidates


    @_profiling
    def _shingle_ngram_candidates(self, corpus, n_size):
        # NOTE: generate ngrams via list comprehension is 2 times faster than
        # via re.findall when corpus size is about 13MB
        total = len(corpus)
        ngrams = [corpus[i : i+n_size] for i in xrange(total - n_size + 1)]
        return ngrams


    def _compute_pmi(self, xy_cnt, x_cnt, y_cnt, norm = False):
        """
        The defination of (N)PMI referred from the following paper:
        Normalized (Pointwise) Mutual Information in Collocation Extraction
        """
        if 0 == x_cnt or 0 == y_cnt:
            return 0
        pmi = math.log(1.0 * self._char_cnt * xy_cnt / (x_cnt * y_cnt))
        if norm:
            pmi /= (-1 * math.log(1.0 * xy_cnt / self._char_cnt))
        return pmi


    def _compute_entropy(self, counter_series):
        total_cnt = counter_series.sum()
        freq_series = counter_series / total_cnt
        entropy = -1 * (freq_series.apply(log) * freq_series).sum()
        return entropy


if '__main__' == __name__:
    fpath = sys.argv[1] 
    out_fpath = sys.argv[2] 
    extractor = Extractor(max_ngrams=5, min_freq=20, min_support=3.6,
        entropy_threshold=1.55)
    extractor.run(fpath, out_fpath)
