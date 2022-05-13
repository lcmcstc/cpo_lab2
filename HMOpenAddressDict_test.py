import unittest
from hypothesis import given
import hypothesis.strategies as st
from HMOpenAddressDict import *


class TestHMOpenAddressDict(unittest.TestCase):

    def test_api(self):
        empty = mempty()
        l1 = cons(None, "c", cons(2, "b", cons("a", 1, empty)))
        l2 = cons("a", 1, cons(None, "c", cons(2, "b", empty)))
        self.assertEqual(str(empty), "{}")
        self.assertTrue(
            str(l1) in ["{'a':1,2:'b',None:'c'}",
                        "{'a':1,None:'c',2:'b'}",
                        "{2:'b','a':1,None:'c'}",
                        "{2: 'b', None: 'c', 'a': 1}",
                        "{None: 'c', 2: 'b', 'a': 1}",
                        "{None: 'c', 'a': 1, 2: 'b'}"
                        ])
        self.assertNotEqual(empty, l1)
        self.assertNotEqual(empty, l2)
        self.assertEqual(l1, l2)
        self.assertEqual(length(empty), 0)
        self.assertEqual(length(l1), 3)
        self.assertEqual(length(l2), 3)
        self.assertTrue(str(remove(l1, None)) in
                        ["{2:'b','a':1}", "{'a':1,2:'b'}"])
        self.assertTrue(str(remove(l1, 'a')) in
                        ["{2:'b',None:'c'}", "{None:'c',2:'b'}"])
        self.assertFalse(member(None, empty))
        self.assertTrue(member(None, l1))
        self.assertTrue(member('a', l1))
        self.assertTrue(member(2, l1))
        self.assertFalse(member(3, l1))
        self.assertEqual(l1, from_list([('a', 1), (2, 'b'), (None, 'c')]))
        self.assertEqual(l1, from_list(
            [(2, 'B'), ('a', 1), (2, 'b'), (None, 'c')]))
        self.assertEqual(mconcat(l1, l2), from_list(
            [(2, 'B'), ('a', 1), (2, 'b'), (None, 'c')]))
        buf = []
        for e in l1:
            buf.append(e)
        self.assertEqual(filter(l1, lambda e1: e1 is None),
                         cons(None, "c", empty))
        self.assertEqual(
            map(l1, lambda x: (x[0], str(x[1]) + "a")),
            cons(None, "ca", cons(2, "ba", cons("a", "1a", empty))))
        l3 = cons(None, 1, cons(2, 2, cons("a", 3, empty)))
        self.assertEqual(reduce(l3, lambda x, y: x + y), 6)
        self.assertEqual(empty, mempty())

    def test_size(self):
        empty = mempty()
        self.assertEqual(length(mempty()), 0)
        self.assertEqual(length(cons("a", 1, empty)), 1)
        self.assertEqual(length(cons("a", 1,
                                     cons(None, "c", cons(2, "b", empty)))), 3)

    def test_cons(self):
        empty = mempty()
        l1 = cons(None, "c", cons(2, "b", cons("a", 1, empty)))
        l2 = cons("a", 1, cons(None, "c", cons(2, "b", empty)))
        self.assertNotEqual(empty, l1)
        self.assertNotEqual(empty, l2)
        self.assertEqual(l1, l2)

    def test_remove(self):
        empty = mempty()
        l1 = cons(None, "c", cons(2, "b", cons("a", 1, empty)))
        l2 = cons(None, "c", cons(2, "b", cons("a", 1, empty)))
        l3 = remove(l1, None)
        l4 = remove(l1, 'a')
        self.assertEqual(l1, l2)
        self.assertEqual(l3, cons(2, "b", cons("a", 1, empty)))
        self.assertEqual(l4, cons(None, "c", cons(2, "b", empty)))

    def test_reverse(self):
        empty = mempty()
        l1 = cons(None, "c", cons(2, "b", cons("a", 1, empty)))
        l2 = from_list([(None, 'c'), (2, 'b'), ('a', 1)])
        l3 = reverse(l1)
        self.assertEqual(str(l3), str(l2))

    def test_mconcat(self):
        empty = mempty()
        l1 = cons(None, "c", cons(2, "b", cons("a", 1, empty)))
        l2 = cons("a", 1, cons(None, "c", cons(2, "b", empty)))
        self.assertEqual(mconcat(empty, empty), empty)
        self.assertEqual(mconcat(cons("a", 1, empty), empty),
                         cons("a", 1, empty))
        self.assertEqual(mconcat(empty, cons("a", 1, empty)),
                         cons("a", 1, empty))
        self.assertEqual(mconcat(l1, l2), from_list(
            [(2, 'B'), ('a', 1), (2, 'b'), (None, 'c')]))
        self.assertEqual(mconcat(mconcat(l1, l2), cons(90, 89, empty)),
                         from_list([(2, 'B'), ('a', 1), (2, 'b'),
                                    (None, 'c'), (90, 89)]))

    def test_to_list(self):
        empty = mempty()
        self.assertEqual(to_list(empty), [])
        self.assertEqual(to_list(cons("a", 1, empty)), [("a", 1)])
        self.assertEqual(to_list(cons(2, "b",
                        cons("a", 1, empty))), [("a", 1), (2, "b")])

    def test_from_list(self):
        test_data = [
            [('a', 1), (2, 'b'), (None, 'c')],
            [('a', 1), (2, 'b')],
            [('a', 1)]
        ]
        for e in test_data:
            self.assertEqual(to_list(from_list(e)), e)

    @given(st.dictionaries(st.integers(), st.integers()))
    def test_from_list_to_list_equality(self, a):
        # first convert the dict to list[tuple],
        # it is order removing duplicate keys
        test = exchangeDic2Tuples(a)
        self.assertEqual(to_list(from_list(test)), test)

    @given(a=st.dictionaries(st.integers(), st.integers()),
           b=st.dictionaries(st.integers(), st.integers()),
           c=st.dictionaries(st.integers(), st.integers()))
    def test_monoid_identity(self, a, b, c):
        empty = mempty()
        # first convert the dict to list[tuple],
        # it is order removing duplicate keys
        # (a+b)+c=a+(b+c)
        md_a = from_list(exchangeDic2Tuples(a))
        md_b = from_list(exchangeDic2Tuples(b))
        md_c = from_list(exchangeDic2Tuples(c))
        # (a+b)+c
        r_one = mconcat(mconcat(md_a, md_b), md_c)
        md_a = from_list(exchangeDic2Tuples(a))
        md_b = from_list(exchangeDic2Tuples(b))
        md_c = from_list(exchangeDic2Tuples(c))
        # a+(b+c)
        r_two = mconcat(md_a, mconcat(md_b, md_c))
        self.assertEqual(r_two, r_one)

        # a+{}=a,{}+a=a
        self.assertEqual(mconcat(from_list(exchangeDic2Tuples(a)), empty),
                         from_list(exchangeDic2Tuples(a)))
        self.assertEqual(mconcat(empty, from_list(exchangeDic2Tuples(a))),
                         from_list(exchangeDic2Tuples(a)))

    def test_iter(self):
        tlist = [(1, 1), (2, 2), (3, 3)]
        myd = from_list(tlist)
        tmp = []
        for e in myd:
            t = (e[0], e[1])
            tmp.append(t)
        self.assertEqual(tlist, tmp)
        self.assertEqual(to_list(myd), tmp)

    def test_find(self):
        md = HMOpenAddressDict(2)
        md.add(None, 1)
        md.add(2, None)
        self.assertEqual(1, find(md, None))
        self.assertEqual(None, find(md, 2))

    def test_filter(self):
        l1 = cons(None, "c", cons(2, "b", cons("a", 1, mempty())))
        self.assertEqual(filter(l1, lambda e1: e1 is None),
                         cons(None, "c", mempty()))

    def test_map(self):
        l1 = cons(None, "c", cons(2, "b", cons("a", 1, mempty())))
        self.assertEqual(map(l1, lambda x: (x[0], str(x[1]) + "a")),
                         cons(None, "ca", cons(2, "ba",
                                               cons("a", "1a", mempty()))))

    def test_reduce(self):
        l3 = cons(None, 1, cons(2, 2, cons("a", 3, mempty())))
        self.assertEqual(reduce(l3, lambda x, y: x + y), 6)

    def test_empty(self):
        t1 = from_list([])
        self.assertEqual(mempty(), t1)

    @given(st.dictionaries(st.integers(), st.integers()))
    def test_python_len_and_list_size_equality(self, a):
        test = exchangeDic2Tuples(a)
        self.assertEqual(length(from_list(test)), len(a))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    unittest.main()
