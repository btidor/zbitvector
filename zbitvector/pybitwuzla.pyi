# Generated from https://github.com/bitwuzla/bitwuzla at 1230d80

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Tuple

class Bitwuzla:
    def assert_formula(self, formula: BitwuzlaTerm) -> None:
        """assert_formula(formula,...)

        Assert one or more formulas.

        :param formula: Boolean term.
        :type formula: BitwuzlaTerm"""
        ...
    def assume_formula(self, formula: BitwuzlaTerm) -> None:
        """assume_formula(formula,...)

        Assume one or more formulas.

        You must enable incremental usage via
        :func:`~pybitwuzla.Bitwuzla.set_option` before you can add
        assumptions.
        In contrast to assertions added via
        :func:`~pybitwuzla.Bitwuzla.assert_formula`, assumptions
        are discarded after each call to
        :func:`~pybitwuzla.Bitwuzla.check_sat`.
        Assumptions and assertions are logically combined via Boolean
        *and*.
        Assumption handling in Bitwuzla is analogous to assumptions
        in MiniSAT.

        :param formula: Boolean term.
        :type formula: BitwuzlaTerm"""
        ...
    def check_sat(self) -> Result:
        """Check satisfiability of asserted and assumed input formulas.

        Input formulas can either be asserted via
        :func:`~pybitwuzla.Bitwuzla.assert_formula` or
        assumed via :func:`~pybitwuzla.Bitwuzla.assume_formula`.

        If this function is called multiple times it is required to
        enable incremental usage via :func:`~pybitwuzla.Bitwuzla.set_opt`.

        :return: - :class:`~pybitwuzla.Result.SAT` if the input formula is
                   satisfiable (under possibly given assumptions)
                 - :class:`~pybitwuzla.Result.UNSAT` if it is unsatisfiable
                 - :class:`~pybitwuzla.Result.UNKNOWN` otherwise
        :rtype: Result

        .. note::
            Assertions and assumptions are combined via Boolean *and*.

        .. seealso::
            :func:`~pybitwuzla.Bitwuzla.get_value`,
            :func:`~pybitwuzla.Bitwuzla.get_value_str`"""
        ...
    def copyright(self) -> str:
        """:return: The copyright information.
        :rtype: str"""
        ...
    def dump_formula(self, fmt: str = "smt2") -> str:
        """dump_formula(fmt = "smt2")

        Dump the current formula as a string in format ``fmt``.

        :param fmt: Model format. Available formats: "btor", "smt2"
        :type fmt: str = "smt2"

        :return: String representation of formula in format ``fmt``.
        :rtype: str"""
        ...
    def fixate_assumptions(self) -> None:
        """Assert all assumptions added since the last
        :func:`~pybitwuzla.Bitwuzla.check_sat` call as assertions.

        .. seealso::
             :func:`~pybitwuzla.Bitwuzla.assume_formula`."""
        ...
    def get_model(self, fmt: str = "smt2") -> str:
        """get_model(fmt = "smt2")

        Get the model as a string in format ``fmt``.

        :param fmt: Model format. Available formats: "btor", "smt2"
        :type fmt: str = "smt2"

        :return: String representation of model in format ``fmt``.
        :rtype: str"""
        ...
    def get_option(self, opt: Option) -> None:
        """get_option(opt)

        Get the current value of option ``opt``.

        :param opt: Option.
        :type opt: BitwuzlaOption
        :return: Option value.

        .. seealso::
             For a list of available options see :class:`~pybitwuzla.Option`"""
        ...
    def get_unsat_assumptions(self) -> List[BitwuzlaTerm]:
        """Return list of unsatisfiable assumptions previously added via
        :func:`~pybitwuzla.Bitwuzla.assume_formula`.

        Requires that the last :func:`~pybitwuzla.Bitwuzla.check_sat` call
        returned `~pybitwuzla.Result.UNSAT`.

        :return:  List of unsatisfiable assumptions
        :rtype:   list(BitwuzlaTerm)"""
        ...
    def get_unsat_core(self) -> List[BitwuzlaTerm]:
        """Return list of unsatisfiable assertions previously added via
        :func:`~pybitwuzla.Bitwuzla.assert_formula`.

        Requires that the last :func:`~pybitwuzla.Bitwuzla.check_sat` call
        returned :class:`~pybitwuzla.Result.UNSAT`.

        :return:  list of unsatisfiable assertions
        :rtype:   list(BitwuzlaTerm)"""
        ...
    def get_value(self, term: BitwuzlaTerm) -> BitwuzlaTerm:
        """get_value(term)

        Get model value of term.

        Requires that the last :func:`~pybitwuzla.Bitwuzla.check_sat` call
        returned `~pybitwuzla.Result.SAT`.

        :type term: BitwuzlaTerm
        :return: Term representing the model value of `term`.
        :rtype: BitwuzlaTerm"""
        ...
    def get_value_str(self, term: BitwuzlaTerm) -> Any:
        """get_value_str(term)

        Get string representation of model value of a `term`.

        Requires that the last :func:`~pybitwuzla.Bitwuzla.check_sat` call
        returned :class:`~pybitwuzla.Result.SAT`.

        :type term: BitwuzlaTerm
        :rtype: Any
        :return:
            - arrays: dictionary mapping indices to values
            - bit-vectors: bit string
            - floating-points: 3-tuple of bit strings
              (sign, exponent, significand)
            - functions: dictionary mapping tuples of arguments to values
            - rounding mode: string representation of rounding mode value"""
        ...
    def git_id(self) -> str:
        """:return: The git commit sha.
        :rtype: str"""
        ...
    def is_unsat_assumption(self, assumption: BitwuzlaTerm) -> List[bool]:
        """is_unsat_assumption(assumption,...)

        Determine if any of the given assumptions are false assumptions.

        Unsat assumptions are those assumptions that force an
        input formula to become unsatisfiable.
        Unsat assumptions handling in Bitwuzla is analogous to
        unsatisfiable assumptions in MiniSAT.

        See :func:`~pybitwuzla.Bitwuzla.assume_formula`.

        :param assumption: Boolean terms.
        :type assumption:  BitwuzlaTerm
        :return:  List of Boolean values, where True indicates that the
                  assumption at given index is true or false.
        :rtype:   list(bool)"""
        ...
    def mk_array_sort(self, index: BitwuzlaSort, elem: BitwuzlaSort) -> BitwuzlaSort:
        """mk_array_sort(index, elem)

        Create array sort with given index and element sorts.

        :param index: The sort of the array index.
        :type index: BitwuzlaSort
        :param elem: The sort of the array elements.
        :type elem: BitwuzlaSort

        :return:  Array sort.
        :rtype: BitwuzlaSort"""
        ...
    def mk_bool_sort(self) -> BitwuzlaSort:
        """Create a Boolean sort.

        :return: Sort of type Boolean.
        :rtype: BitwuzlaSort"""
        ...
    def mk_bv_max_signed(self, sort: BitwuzlaSort) -> BitwuzlaTerm:
        """mk_bv_max_signed(sort)

        Create a bit-vector maximum signed value.

        :param sort: Bit-vector sort.
        :type sort: BitwuzlaSort

        :return: A term representing the bit-vector value of given sort
                 where the MSB is set to 0 and all remaining bits are set to
                 1.
        :rtype: BitwuzlaTerm"""
        ...
    def mk_bv_min_signed(self, sort: BitwuzlaSort) -> BitwuzlaTerm:
        """mk_bv_min_signed(sort)

        Create a bit-vector minimum signed value.

        :param sort: Bit-vector sort.
        :type sort: BitwuzlaSort

        :return: A term representing the bit-vector value of given sort
                 where the MSB is set to 1 and all remaining bits are set to
                 0.
        :rtype: BitwuzlaTerm"""
        ...
    def mk_bv_ones(self, sort: BitwuzlaSort) -> BitwuzlaTerm:
        """mk_bv_ones(sort)

        Create a bit-vector value with ``sort`` where all bits are set to 1.

        :param sort: Bit-vector sort.
        :type sort: BitwuzlaSort

        :return: A term representing the bit-vector value of given sort
                 where all bits are set to 1.
        :rtype: BitwuzlaTerm"""
        ...
    def mk_bv_sort(self, width: int) -> BitwuzlaSort:
        """mk_bv_sort(width)

        Create bit-vector sort of size ``width``.

        :param width: Bit width.
        :type width: uint32_t

        :return:  Bit-vector sort of bit width ``width``.
        :rtype: pybitwuzla.BitwuzlaSort"""
        ...
    def mk_bv_value(self, sort: BitwuzlaSort, value: str | int) -> BitwuzlaTerm:
        """mk_bv_value(sort, value)

        Create bit-vector ``value`` with given ``sort``.

        :param sort: Bit-vector sort.
        :type sort: BitwuzlaSort
        :param value: Hexadecimal, binary or decimal value.

                      - hexadecimal prefix: ``0x`` or ``#x``
                      - binary prefix: ``0b`` or ``#b``
        :type value: str or int

        :return: A term representing the bit-vector value.
        :rtype: BitwuzlaTerm"""
        ...
    def mk_const(self, sort: BitwuzlaSort, symbol: str | None = None) -> BitwuzlaTerm:
        """mk_const(sort, symbol = None)

        Create a (first-order) constant of given ``sort`` with ``symbol``.

        :param sort: The sort of the constant.
        :type sort: BitwuzlaSort
        :param symbol: The symbol of the constant.
        :type symbol: str or None = None

        :return: A term representing the constant.
        :rtype: BitwuzlaTerm"""
        ...
    def mk_const_array(self, sort: BitwuzlaSort, value: BitwuzlaTerm) -> BitwuzlaTerm:
        """mk_const_array(sort, value)

        Create a one-dimensional constant array of given sort, initialized
        with given value.

        :param sort: The sort of the array.
        :type sort: BitwuzlaSort
        :param value: The term to initialize the elements of the array with.
        :type value: BitwuzlaTerm

        :return: A term representing a constant array of given sort.
        :rtype: BitwuzlaTerm"""
        ...
    def mk_fp_nan(self, sort: BitwuzlaSort) -> BitwuzlaTerm:
        """mk_fp_nan(sort)

        Create a floating-point NaN value.

        :param sort: Floating-point sort.
        :type sort: BitwuzlaSort

        :return: A term representing the floating-point NaN value of given
                 floating-point sort.
        :rtype: BitwuzlaTerm"""
        ...
    def mk_fp_neg_inf(self, sort: BitwuzlaSort) -> BitwuzlaTerm:
        """mk_fp_neg_inf(sort)

        Create a floating-point negative infinity value (SMT-LIB: `-oo`).

        :param sort: Floating-point sort.
        :type sort: BitwuzlaSort

        :return: A term representing the floating-point negative infinity
                 value of given floating-point sort.
        :rtype: BitwuzlaTerm"""
        ...
    def mk_fp_neg_zero(self, sort: BitwuzlaSort) -> BitwuzlaTerm:
        """mk_fp_neg_zero(sort)

        Create a floating-point negative zero value (SMT-LIB: `-zero`).

        :param sort: Floating-point sort.
        :type sort: BitwuzlaSort

        :return: A term representing the floating-point negative zero value
                 of given floating-point sort.
        :rtype: BitwuzlaTerm"""
        ...
    def mk_fp_pos_inf(self, sort: BitwuzlaSort) -> BitwuzlaTerm:
        """mk_fp_pos_inf(sort)

        Create a floating-point positive infinity value (SMT-LIB: `+oo`).

        :param sort: Floating-point sort.
        :type sort: BitwuzlaSort

        :return: A term representing the floating-point positive infinity
                 value of given floating-point sort.
        :rtype: BitwuzlaTerm"""
        ...
    def mk_fp_pos_zero(self, sort: BitwuzlaSort) -> BitwuzlaTerm:
        """mk_fp_pos_zero(sort)

        Create a floating-point positive zero value (SMT-LIB: `+zero`).

        :param sort: Floating-point sort.
        :type sort: BitwuzlaSort

        :return: A term representing the floating-point positive zero value
                 of given floating-point sort.
        :rtype: BitwuzlaTerm"""
        ...
    def mk_fp_sort(self, exp_size: int, sig_size: int) -> BitwuzlaSort:
        """mk_fp_sort(exp_size, sig_size)

        Create a floating-point sort with given exponent size ``exp_size``
        and significand size ``sig_size``.

        :param exp_size: Exponent size.
        :type exp_size: uint32_t
        :param sig_size: Significand size.
        :type sig_size: uint32_t

        :return: Floating-point sort.
        :rtype: BitwuzlaSort"""
        ...
    def mk_fp_value(
        self,
        sort: BitwuzlaSort,
        sign: str | int,
        exponent: str | int,
        significand: str | int,
    ) -> BitwuzlaTerm:
        """mk_fp_value(sort, sign, exponent, significand)

        Create a floating-point value from its IEEE 754 standard
        representation given as three bit-vector values representing the
        sign bit, the exponent and the significand.

        :param sort: Floating-point sort.
        :type sort: BitwuzlaSort
        :param sign: The sign bit.
        :type sign: str or int
        :param exponent: The exponent bit-vector value.
        :type exponent: str or int
        :param significand: The significand bit-vector value.
        :type significand: str or int

        :return: A term representing the floating-point value.
        :rtype: BitwuzlaTerm

        .. seealso::
          :func:`~pybitwuzla.Bitwuzla.mk_bv_value` for the supported value
          format for ``sign``, ``exponent``, and ``significand``."""
        ...
    def mk_fp_value_from(
        self, sort: BitwuzlaSort, rm: BitwuzlaTerm, value: str
    ) -> BitwuzlaTerm:
        """mk_fp_value_from(sort, rm, value)

        Create a floating-point value from its real or rational
        representation, given as a string, with respect to given
        rounding mode.

        :param sort: Floating-point sort.
        :type sort: BitwuzlaSort
        :param rm: Rounding mode.
        :type rm: BitwuzlaTerm
        :param value: String representation of real or rational value to
                      create. The expected format for rational values is
                      <numerator>/<denominator>.
        :type value: str

        :return: A term representing the real or rational value as floating
                 point value with given sort.
        :rtype: BitwuzlaTerm"""
        ...
    def mk_fun_sort(self, domain: List[Any], codomain: BitwuzlaSort) -> BitwuzlaSort:
        """mk_fun_sort(domain, codomain)

        Create function sort with given domain and codomain.

        :param domain: A list of all the function arguments' sorts.
        :type domain: list
        :param codomain: The sort of the function's return value.
        :type codomain: BitwuzlaSort

        :return:  Function sort, which maps ``domain`` to ``codomain``.
        :rtype: BitwuzlaSort"""
        ...
    def mk_rm_sort(self) -> BitwuzlaSort:
        """mk_rm_sort()

        Create a rounding mode sort.

        :return: Rounding mode sort.
        :rtype: BitwuzlaSort"""
        ...
    def mk_rm_value(self, rm: RoundingMode) -> BitwuzlaTerm:
        """mk_rm_value(rm)

        Create a rounding mode value.

        :param rm: Rounding mode.
        :type rm: RoundingMode

        :return: A term representing the rounding mode value.
        :rtype: BitwuzlaTerm"""
        ...
    def mk_term(
        self,
        kind: Kind,
        terms: List[BitwuzlaTerm] | Tuple[BitwuzlaTerm, ...],
        indices: Tuple[int, ...] | None = None,
    ) -> BitwuzlaTerm:
        """mk_term(kind, terms, indices = None)

        Create a term of given kind with the given argument terms.

        :param kind: The operator kind.
        :type kind: Kind
        :param terms: The argument terms.
        :type terms: list(BitwuzlaTerm) or tuple(BitwuzlaTerm, ...)
        :param indices: The argument indices.
        :type indices: tuple(int, ...) or None = None

        :return: A term representing an operation of given kind.
        :rtype: BitwuzlaTerm"""
        ...
    def mk_var(self, sort: BitwuzlaSort, symbol: str | None = None) -> BitwuzlaTerm:
        """mk_var(sort, symbol = None)

        Create a variable of given ``sort`` with ``symbol``.

        :param sort: The sort of the variable.
        :type sort: BitwuzlaSort
        :param symbol: The symbol of the variable.
        :type symbol: str or None = None

        :return: A term representing the variable.
        :rtype: BitwuzlaTerm

        .. note::
             This creates a variable to be bound by terms of kind
             :class:`~pybitwuzla.Kind.LAMBDA`."""
        ...
    def pop(self, levels: int = 1) -> None:
        """pop(levels = 1)

        Pop context levels.

        :param levels: Number of levels to pop.
        :type levels: int = 1

        .. note::
          Assumptions added via :func:`~pybitwuzla.Bitwuzla.assume_formula`
          are not affected by context level changes and are only valid
          until the next :func:`~pybitwuzla.Bitwuzla.check_sat` call no matter
          at what level they were assumed.

        .. seealso::
            :func:`~pybitwuzla.Bitwuzla.assume_formula`"""
        ...
    def push(self, levels: int = 1) -> None:
        """push(levels = 1)

        Push new context levels.

        :param levels: Number of context levels to create.
        :type levels: int = 1

        .. note::
          Assumptions added via :func:`~pybitwuzla.Bitwuzla.assume_formula`
          are not affected by context level changes and are only valid
          until the next :func:`~pybitwuzla.Bitwuzla.check_sat` call no matter
          at what level they were assumed.

        .. seealso::
            :func:`~pybitwuzla.Bitwuzla.assume_formula`"""
        ...
    def reset_assumptions(self) -> None:
        """Remove all assumptions added since the last
        :func:`~pybitwuzla.Bitwuzla.check_sat` call.

        .. seealso::
             :func:`~pybitwuzla.Bitwuzla.assume_formula`."""
        ...
    def set_option(self, opt: Option, value: str | Option | int) -> None:
        """set_option(opt, value)

        Set option ``opt`` to ``value``.

        :param opt:   Option.
        :type opt:    BitwuzlaOption
        :param value: Option value.
        :type value:  str or BitwuzlaOption or int

        .. seealso::
             For a list of available options see :class:`~pybitwuzla.Option`"""
        ...
    def simplify(self) -> Result:
        """Simplify current input formula.

        :return: - :class:`~pybitwuzla.Result.SAT` if the input formula is
                   satisfiable (under possibly given assumptions)
                 - :class:`~pybitwuzla.Result.UNSAT` if it is unsatisfiable
                 - :class:`~pybitwuzla.Result.UNKNOWN` otherwise
        :rtype: Result

        .. note::
            Each call to :func:`~pybitwuzla.Bitwuzla.check_sat`
            simplifies the input formula as a preprocessing step."""
        ...
    def substitute(
        self,
        terms: List[BitwuzlaTerm] | Tuple[BitwuzlaTerm, ...] | BitwuzlaTerm,
        subst_map: Dict[BitwuzlaTerm, BitwuzlaTerm],
    ) -> List[BitwuzlaTerm]:
        """substitute(terms, subst_map)

        Substitute constants or variables in ``terms`` by applying
        substitutions in ``subst_map``.

        :param terms: List of terms to apply substitutions.
        :type terms: list(BitwuzlaTerm) or tuple(BitwuzlaTerm, ...) or BitwuzlaTerm
        :param subst_map: The substitution map mapping constants or
                          variables to terms.
        :type subst_map: dict(BitwuzlaTerm,BitwuzlaTerm)

        :return: List of terms with substitutions applied.
        :rtype: list(BitwuzlaTerm)"""
        ...
    def version(self) -> str:
        """:return: The version number.
        :rtype: str"""
        ...

class BitwuzlaException(Exception): ...

class BitwuzlaSort:
    def array_get_element(self) -> BitwuzlaSort:
        """Get element sort of array sort.

        :return: Element sort.
        :rtype: BitwuzlaSort"""
        ...
    def array_get_index(self) -> BitwuzlaSort:
        """Get index sort of array sort.

        :return: Index sort.
        :rtype: BitwuzlaSort"""
        ...
    def bv_get_size(self) -> int:
        """Get size of bit-vector sort.

        :return: Size of bit-vector sort.
        :rtype: int"""
        ...
    def fp_get_exp_size(self) -> int:
        """Get size of exponent of floating-point sort.

        :return: Size of exponent.
        :rtype: int"""
        ...
    def fp_get_sig_size(self) -> int:
        """Get size of significand of floating-point sort.

        :return: Size of significand.
        :rtype: int"""
        ...
    def fun_get_arity(self) -> int:
        """Get arity of function sort.

        :return: Function arity.
        :rtype: int"""
        ...
    def fun_get_codomain(self) -> BitwuzlaSort:
        """Get codomain sort of function sort.

        :return: Codomain sort.
        :rtype: BitwuzlaSort"""
        ...
    def fun_get_domain_sorts(self) -> List[BitwuzlaSort]:
        """Get domain sorts of function sort.

        :return: Domain sorts.
        :rtype: list(BitwuzlaSort)"""
        ...
    def is_array(self) -> bool:
        """:return: True if sort is an array sort, False otherwise.
        :rtype: bool"""
        ...
    def is_bv(self) -> bool:
        """:return: True if sort is a bit-vector sort, False otherwise.
        :rtype: bool"""
        ...
    def is_fp(self) -> bool:
        """:return: True if sort is a floating-point sort, False otherwise.
        :rtype: bool"""
        ...
    def is_fun(self) -> bool:
        """:return: True if sort is a function sort, False otherwise.
        :rtype: bool"""
        ...
    def is_rm(self) -> bool:
        """:return: True if sort is a rounding mode sort, False otherwise.
        :rtype: bool"""
        ...

class BitwuzlaTerm:
    def dump(self, fmt: str = "smt2") -> str:
        """dump(fmt = "smt2")

        Get string representation of term in format ``fmt``.

        :param fmt: Output format. Available formats: "btor", "smt2"
        :type fmt: str = "smt2"

        :return: String representation of the term in format ``fmt``.
        :rtype: str"""
        ...
    def get_children(self) -> List[BitwuzlaTerm]:
        """:return: The children of the term.
        :rtype: list(BitwuzlaTerm)"""
        ...
    def get_indices(self) -> List[int]:
        """:return: Indices of indexed operator.
        :rtype: list(int)"""
        ...
    def get_kind(self) -> Kind:
        """:return: Operator kind of term.
        :rtype: Kind"""
        ...
    def get_sort(self) -> BitwuzlaSort:
        """:return: The sort of the term.
        :rtype: BitwuzlaSort"""
        ...
    def get_symbol(self) -> str | None:
        """:return: The symbol of the term.
        :rtype: str or None

        .. seealso::
            :func:`~pybitwuzla.BitwuzlaTerm.set_symbol`"""
        ...
    def is_array(self) -> bool:
        """:return: True if term is an array, False otherwise.
        :rtype: bool"""
        ...
    def is_bound_var(self) -> bool:
        """:return: True if term is a bound variable, False otherwise.
        :rtype: bool"""
        ...
    def is_bv(self) -> bool:
        """:return: True if term is a bit-vector, False otherwise.
        :rtype: bool"""
        ...
    def is_bv_value(self) -> bool:
        """:return: True if term is a bit-vector value, False otherwise.
        :rtype: bool"""
        ...
    def is_bv_value_max_signed(self) -> bool:
        """:return: True if term is a bit-vector maximum signed value,
                 False otherwise.
        :rtype: bool"""
        ...
    def is_bv_value_min_signed(self) -> bool:
        """:return: True if term is a bit-vector minimum signed value,
                 False otherwise.
        :rtype: bool"""
        ...
    def is_bv_value_one(self) -> bool:
        """:return: True if term is a bit-vector value one, False otherwise.
        :rtype: bool"""
        ...
    def is_bv_value_ones(self) -> bool:
        """:return: True if term is a bit-vector value ones, False otherwise.
        :rtype: bool"""
        ...
    def is_bv_value_zero(self) -> bool:
        """:return: True if term is a bit-vector value zero, False otherwise.
        :rtype: bool"""
        ...
    def is_const(self) -> bool:
        """:return: True if term is a constant, False otherwise.
        :rtype: bool"""
        ...
    def is_const_array(self) -> bool:
        """:return: True if term is a constant array, False otherwise.
        :rtype: bool"""
        ...
    def is_fp(self) -> bool:
        """:return: True if term is a floating-point, False otherwise.
        :rtype: bool"""
        ...
    def is_fp_value(self) -> bool:
        """:return: True if term is a floating-point value, False otherwise.
        :rtype: bool"""
        ...
    def is_fp_value_nan(self) -> bool:
        """:return: True if term is a floating-point NaN value,
                 False otherwise.
        :rtype: bool"""
        ...
    def is_fp_value_neg_inf(self) -> bool:
        """:return: True if term is a floating-point negative infinity value,
                 False otherwise.
        :rtype: bool"""
        ...
    def is_fp_value_neg_zero(self) -> bool:
        """:return: True if term is a floating-point negative zero value,
                 False otherwise.
        :rtype: bool"""
        ...
    def is_fp_value_pos_inf(self) -> bool:
        """:return: True if term is a floating-point positive infinity value,
                 False otherwise.
        :rtype: bool"""
        ...
    def is_fp_value_pos_zero(self) -> bool:
        """:return: True if term is a floating-point positive zero value,
                 False otherwise.
        :rtype: bool"""
        ...
    def is_fun(self) -> bool:
        """:return: True if term is a function, False otherwise.
        :rtype: bool"""
        ...
    def is_indexed(self) -> bool:
        """:return: True if term is indexed, False otherwise.
        :rtype: bool"""
        ...
    def is_rm(self) -> bool:
        """:return: True if term is a rounding mode, False otherwise.
        :rtype: bool"""
        ...
    def is_rm_value(self) -> bool:
        """:return: True if term is a rounding mode value, False otherwise.
        :rtype: bool"""
        ...
    def is_var(self) -> bool:
        """:return: True if term is a variable, False otherwise.
        :rtype: bool"""
        ...
    def set_symbol(self, symbol: str) -> None:
        """set_symbol(symbol)

        Set the symbol of the term.

        :param symbol: Symbol of the term.
        :type symbol: str"""
        ...

class Kind(Enum):
    """BitwuzlaTerm kinds. For more information on term kinds see :ref:`c_kinds`."""

    CONST = 0
    CONST_ARRAY = 1
    VAL = 2
    VAR = 3
    AND = 4
    APPLY = 5
    ARRAY_SELECT = 6
    ARRAY_STORE = 7
    BV_ADD = 8
    BV_AND = 9
    BV_ASHR = 10
    BV_COMP = 11
    BV_CONCAT = 12
    BV_DEC = 13
    BV_INC = 14
    BV_MUL = 15
    BV_NAND = 16
    BV_NEG = 17
    BV_NOR = 18
    BV_NOT = 19
    BV_OR = 20
    BV_REDAND = 21
    BV_REDOR = 22
    BV_REDXOR = 23
    BV_ROL = 24
    BV_ROR = 25
    BV_SADD_OVERFLOW = 26
    BV_SDIV_OVERFLOW = 27
    BV_SDIV = 28
    BV_SGE = 29
    BV_SGT = 30
    BV_SHL = 31
    BV_SHR = 32
    BV_SLE = 33
    BV_SLT = 34
    BV_SMOD = 35
    BV_SMUL_OVERFLOW = 36
    BV_SREM = 37
    BV_SSUB_OVERFLOW = 38
    BV_SUB = 39
    BV_UADD_OVERFLOW = 40
    BV_UDIV = 41
    BV_UGE = 42
    BV_UGT = 43
    BV_ULE = 44
    BV_ULT = 45
    BV_UMUL_OVERFLOW = 46
    BV_UREM = 47
    BV_USUB_OVERFLOW = 48
    BV_XNOR = 49
    BV_XOR = 50
    DISTINCT = 51
    EQUAL = 52
    EXISTS = 53
    FORALL = 54
    FP_ABS = 55
    FP_ADD = 56
    FP_DIV = 57
    FP_EQ = 58
    FP_FMA = 59
    FP_FP = 60
    FP_GEQ = 61
    FP_GT = 62
    FP_IS_INF = 63
    FP_IS_NAN = 64
    FP_IS_NEG = 65
    FP_IS_NORMAL = 66
    FP_IS_POS = 67
    FP_IS_SUBNORMAL = 68
    FP_IS_ZERO = 69
    FP_LEQ = 70
    FP_LT = 71
    FP_MAX = 72
    FP_MIN = 73
    FP_MUL = 74
    FP_NEG = 75
    FP_REM = 76
    FP_RTI = 77
    FP_SQRT = 78
    FP_SUB = 79
    IFF = 80
    IMPLIES = 81
    ITE = 82
    LAMBDA = 83
    NOT = 84
    OR = 85
    XOR = 86
    BV_EXTRACT = 87
    BV_REPEAT = 88
    BV_ROLI = 89
    BV_RORI = 90
    BV_SIGN_EXTEND = 91
    BV_ZERO_EXTEND = 92
    FP_TO_FP_FROM_BV = 93
    FP_TO_FP_FROM_FP = 94
    FP_TO_FP_FROM_SBV = 95
    FP_TO_FP_FROM_UBV = 96
    FP_TO_SBV = 97
    FP_TO_UBV = 98

class Option(Enum):
    """Configuration options supported by Bitwuzla. For more information on
    options see :ref:`c_options`."""

    ENGINE = 0
    EXIT_CODES = 1
    INPUT_FORMAT = 2
    INCREMENTAL = 3
    LOGLEVEL = 4
    OUTPUT_FORMAT = 5
    OUTPUT_NUMBER_FORMAT = 6
    PRETTY_PRINT = 7
    PRINT_DIMACS = 8
    PRODUCE_MODELS = 9
    PRODUCE_UNSAT_CORES = 10
    SAT_ENGINE = 11
    SEED = 12
    VERBOSITY = 13
    PP_ACKERMANN = 14
    PP_BETA_REDUCE = 15
    PP_ELIMINATE_EXTRACTS = 16
    PP_ELIMINATE_ITES = 17
    PP_EXTRACT_LAMBDAS = 18
    PP_MERGE_LAMBDAS = 19
    PP_NONDESTR_SUBST = 20
    PP_NORMALIZE_ADD = 21
    PP_SKELETON_PREPROC = 22
    PP_UNCONSTRAINED_OPTIMIZATION = 23
    PP_VAR_SUBST = 24
    RW_EXTRACT_ARITH = 25
    RW_LEVEL = 26
    RW_NORMALIZE = 27
    RW_NORMALIZE_ADD = 28
    RW_SIMPLIFY_CONSTRAINTS = 29
    RW_SLT = 30
    RW_SORT_AIG = 31
    RW_SORT_AIGVEC = 32
    RW_SORT_EXP = 33
    FUN_DUAL_PROP = 34
    FUN_DUAL_PROP_QSORT = 35
    FUN_EAGER_LEMMAS = 36
    FUN_LAZY_SYNTHESIZE = 37
    FUN_JUST = 38
    FUN_JUST_HEURISTIC = 39
    FUN_PREPROP = 40
    FUN_PRESLS = 41
    FUN_STORE_LAMBDAS = 42
    SLS_JUST = 43
    SLS_MOVE_GW = 44
    SLS_MOVE_INC_MOVE_TEST = 45
    SLS_MOVE_PROP = 46
    SLS_MOVE_PROP_FORCE_RW = 47
    SLS_MOVE_PROP_NPROPS = 48
    SLS_MOVE_PROP_NSLSS = 49
    SLS_MOVE_RAND_ALL = 50
    SLS_MOVE_RAND_RANGE = 51
    SLS_MOVE_RAND_WALK = 52
    SLS_MOVE_RANGE = 53
    SLS_MOVE_SEGMENT = 54
    SLS_PROB_MOVE_RAND_WALK = 55
    SLS_NFLIPS = 56
    SLS_STRATEGY = 57
    SLS_USE_RESTARTS = 58
    SLS_USE_BANDIT = 59
    PROP_ASHR = 60
    PROP_CONST_BITS = 61
    PROP_CONST_DOMAINS = 62
    PROP_ENTAILED = 63
    PROP_FLIP_COND_CONST_DELTA = 64
    PROP_FLIP_COND_CONST_NPATHSEL = 65
    PROP_INFER_INEQ_BOUNDS = 66
    PROP_NO_MOVE_ON_CONFLICT = 67
    PROP_NPROPS = 68
    PROP_NUPDATES = 69
    PROP_PATH_SEL = 70
    PROP_PROB_FALLBACK_RANDOM_VALUE = 71
    PROP_PROB_AND_FLIP = 72
    PROP_PROB_EQ_FLIP = 73
    PROP_PROB_FLIP_COND = 74
    PROP_PROB_FLIP_COND_CONST = 75
    PROP_PROB_RANDOM_INPUT = 76
    PROP_PROB_SLICE_FLIP = 77
    PROP_PROB_SLICE_KEEP_DC = 78
    PROP_PROB_USE_INV_VALUE = 79
    PROP_USE_BANDIT = 80
    PROP_USE_INV_LT_CONCAT = 81
    PROP_USE_RESTARTS = 82
    PROP_SEXT = 83
    PROP_SKIP_NO_PROGRESS = 84
    PROP_XOR = 85
    AIGPROP_NPROPS = 86
    AIGPROP_USE_BANDIT = 87
    AIGPROP_USE_RESTARTS = 88
    QUANT_SYNTH_SK = 89
    QUANT_SYNTH_QI = 90
    QUANT_SKOLEM_UF = 91
    QUANT_EAGER_SKOLEM = 92
    QUANT_MBQI = 93
    QUANT_MODE = 94
    CHECK_MODEL = 95
    CHECK_UNCONSTRAINED = 96
    CHECK_UNSAT_ASSUMPTIONS = 97
    DECLSORT_BV_WIDTH = 98
    LS_SHARE_SAT = 99
    PARSE_INTERACTIVE = 100
    SAT_ENGINE_CADICAL_FREEZE = 101
    SAT_ENGINE_LGL_FORK = 102
    SAT_ENGINE_N_THREADS = 103
    SMT_COMP_MODE = 104

class Result(Enum):
    """Satisfiability result."""

    SAT = 10
    UNSAT = 20
    UNKNOWN = 0

class RoundingMode(Enum):
    """Floating-point rounding mode."""

    RNE = 0
    RNA = 1
    RTN = 2
    RTP = 3
    RTZ = 4
