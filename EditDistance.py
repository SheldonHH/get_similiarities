
import os
import csv
import re
import time
import subprocess
import numpy as np
from numpy.linalg import norm
import math
from transformers import AutoTokenizer, AutoModel
import torch
import sys
import multiprocessing
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from simphile import jaccard_similarity, euclidian_similarity, compression_similarity


# text_a = texts[0]
# text_b = keyword

# print(f"Jaccard Similarity: {jaccard_similarity(text_a, text_b)}")
# print(f"Euclidian Similarity: {euclidian_similarity(text_a, text_b)}")
# print(f"Compression Similarity: {compression_similarity(text_a, text_b)}")

        
# def identify_error_pattern_ghidra(error,ErrType):
# 	#print(pattern.patterns)
# 	# print("error:",error)
# 	find_error_pattern = False
# 	for(reg_expression, type_name) in patterns:
# 		out = re.findall(reg_expression, ErrType)
# 		# print("out:",out)
# 		if out:
# 			#print("find")
# 			find_error_pattern = True 
# 			return type_name

def findf(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
            


def EditDistance(word1, word2):
    """
    :type word1: str
    :type word2: str
    :rtype: int
    """
    m = len(word1)
    n = len(word2)
    dp = [[0 for __ in range(m + 1)] for __ in range(n + 1)]
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(n + 1):
        dp[i][0] = i
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            onemore = 1 if word1[j - 1] != word2[i - 1] else 0
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + onemore)
    
    return 1 - dp[i][j]/ max(m,n)











############################################################### main ################################################################


# # for each type number
# def singapore(errTyNum):

        






patterns=[
	(r"\n*((.+?)\d+:\d+:) error: conflicting types for [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*",  "conflicting types for a function"),
	(r"\n*((.+?)\d+:\d+:) error: read-only variable is not assignable", "read-only variable is not assignable"),
	(r"\n*((.+?)\d+:\d+:) error: expected expression","expected expression"),
	(r"\n*((.+?)\d+:\d+:) error: [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* where arithmetic or pointer type is required", 'typecasting pointer'),
	(r"\n*((.+?)\d+:\d+:) error: no member named \'\_[0-9]*\_[0-9]*\_\' in", 'no member named _offset_size_'),
	(r"\n*((.+?)\d+:\d+:) error: no member named \'field\_[a-zA-Z0-9]*\' in", 'no member named field_0x?'),
	(r"\n*((.+?)\d+:\d+:) error: no member named [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* in", 'no member named ?'),
	(r"\n*((.+?)\d+:\d+:) error: invalid operands to binary expression [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*", "invalid operands to binary expression"),
	(r"\n*((.+?)\d+:\d+:) error: member reference type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* is a pointer; did you mean to use '->'\?", "member reference type is a pointer"),
	(r"\n*((.+?)\d+:\d+:) error: member reference type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* is not a pointer", "member reference type is not a pointer"),
	(r"\n*((.+?)\d+:\d+:) error: member reference base type (\'__m128i\'|\'const __m128i\') \([a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*\) is not a structure or union","member reference type '__128i' is not a structure or union"),
	(r"\n*((.+?)\d+:\d+:) error: member reference base type \'__m128\' \([a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*\) is not a structure or union","member reference type '__128' is not a structure or union"),
	(r"\n*((.+?)\d+:\d+:) error: member reference base type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* is not a structure or union","member reference type is not a structure or union"),
	(r"\n*((.+?)\d+:\d+:) error: must use \'struct\' tag to refer to type", "must use 'struct' tag to refer to type"),
	(r"\n*((.+?)\d+:\d+:) error: must use \'enum\' tag to refer to type", "must use 'enum' tag to refer to type"),
	(r"\n*((.+?)\d+:\d+:) error: must use \'union\' tag to refer to type", "must use 'union' tag to refer to type"),
	(r"\n*((.+?)\d+:\d+:) error: must use '(struct|union|enum)' tag to refer to type", "must use '(struct|union|enum)' tag to refer to type"),
	# (r"\n*((.+?)\d+:\d+:) error: use of undeclared identifier \'unk\_[A-Z0-9]*\'", "undeclared identifier with prefix 'unk_'"),
	# (r"\n*((.+?)\d+:\d+:) error: use of undeclared identifier \'byte\_[A-Z0-9]*\'", "undeclared identifier with prefix 'byte_'"),
	# (r"\n*((.+?)\d+:\d+:) error: use of undeclared identifier \'off\_[A-Z0-9]*\'", "undeclared identifier with prefix 'off_'"),
	# (r"\n*((.+?)\d+:\d+:) error: use of undeclared identifier \'[A-Za-z0-9]*\_0\'; did you mean \'[A-Za-z0-9]*\'?", "undeclared identifier with suffix '_0'"),
	# (r"\n*((.+?)\d+:\d+:) error: use of undeclared identifier \'[A-Za-z0-9]*\_1\'; did you mean \'[A-Za-z0-9]*\'?", "undeclared identifier with suffix '_1'"),
	# (r"\n*((.+?)\d+:\d+:) error: use of undeclared identifier \'[A-Za-z0-9]*\_2\'; did you mean \'[A-Za-z0-9]*\'?", "undeclared identifier with suffix '_2'"),
	# (r"\n*((.+?)\d+:\d+:) error: use of undeclared identifier \'[A-Za-z0-9]*\_3\'; did you mean \'[A-Za-z0-9]*\'?", "undeclared identifier with suffix '_3'"),
	# (r"\n*((.+?)\d+:\d+:) error: use of undeclared identifier \'[A-Za-z0-9]*\_4\'; did you mean \'[A-Za-z0-9]*\'?", "undeclared identifier with suffix '_4'"),
	# (r"\n*((.+?)\d+:\d+:) error: use of undeclared identifier \'[A-Za-z0-9]*\_5\'; did you mean \'[A-Za-z0-9]*\'?", "undeclared identifier with suffix '_5'"),
	(r"\n*((.+?)\d+:\d+:) error: use of undeclared identifier \'unk\_[A-Z0-9]*\'", "use of undeclared identifier"),
	(r"\n*((.+?)\d+:\d+:) error: use of undeclared identifier \'byte\_[A-Z0-9]*\'", "use of undeclared identifier"),
	(r"\n*((.+?)\d+:\d+:) error: use of undeclared identifier \'off\_[A-Z0-9]*\'", "use of undeclared identifier"),
	(r"\n*((.+?)\d+:\d+:) error: use of undeclared identifier \'[A-Za-z0-9]*\_0\'; did you mean \'[A-Za-z0-9]*\'?", "use of undeclared identifier"),
	(r"\n*((.+?)\d+:\d+:) error: use of undeclared identifier \'[A-Za-z0-9]*\_1\'; did you mean \'[A-Za-z0-9]*\'?", "use of undeclared identifier"),
	(r"\n*((.+?)\d+:\d+:) error: use of undeclared identifier \'[A-Za-z0-9]*\_2\'; did you mean \'[A-Za-z0-9]*\'?", "use of undeclared identifier"),
	(r"\n*((.+?)\d+:\d+:) error: use of undeclared identifier \'[A-Za-z0-9]*\_3\'; did you mean \'[A-Za-z0-9]*\'?", "use of undeclared identifier"),
	(r"\n*((.+?)\d+:\d+:) error: use of undeclared identifier \'[A-Za-z0-9]*\_4\'; did you mean \'[A-Za-z0-9]*\'?", "use of undeclared identifier"),
	(r"\n*((.+?)\d+:\d+:) error: use of undeclared identifier \'[A-Za-z0-9]*\_5\'; did you mean \'[A-Za-z0-9]*\'?", "use of undeclared identifier"),
	(r"\n*((.+?)\d+:\d+:) error: use of undeclared identifier", "use of undeclared identifier"),
	(r"\n*((.+?)\d+:\d+:) error: operand of type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* cannot be cast to a pointer type","operand of type 'one type' cannot be cast to a pointer type"),
	(r"\n*((.+?)\d+:\d+:) error: unknown type name \'[a-zA-Z]*\_0\'", "unknown type name with suffix '_0'"),
	(r"\n*((.+?)\d+:\d+:) error: (unknown|unexpected) type name", "unknown type name"),
	(r"(In function `{}':\n*((.+?):\d+:\d*:*) undefined reference to `(.*)'|\n*(.+?):\d+:\d+: warning: implicit declaration of function '(.+?)' is invalid in C99 \[-Wimplicit-function-declaration\].*?\n(.+?)\n)", "undefined reference to a function"),
	(r"\n*((.+?)\d+:\d+:) error: expected \'[\;\)\]\(\[\{\}]*\'", "expected ;, ('"),
(r"\n*((.+?)\d+:\d+:) error: array type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* is not assignable", "array type is not assignable"),
(r"\n*((.+?)\d+:\d+:) error: read-only variable is not assignable", "read-only variable is not assignable"),
	(r"\n*((.+?)\d+:\d+:) error: [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* is not assignable", "type 'A' is not assignable"),
	(r"\n*((.+?)\d+:\d+:) error: \#endif without \#if", "#endif without #if"),
	(r"\n*((.+?)\d+:\d+:) error: redefinition of label [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*", "redefinition of label"),
	(r"\n*((.+?)\d+:\d+:) error: redefinition of parameter [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*", "redefinition of parameter"),
	(r"\n*((.+?)\d+:\d+:) error: redefinition of [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* as different kind of symbol", "redefinition of 'A' as different kind of symbol"),
	(r"\n*((.+?)\d+:\d+:) error: [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* cannot be cast to type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*", "cannot be cast to type"),
	(r"\n*((.+?)\d+:\d+:) error: too many arguments to function call[a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*","too many arguments to function call"),
	(r"\n*((.+?)\d+:\d+:) error: too few arguments to function call[a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*","too few arguments to function call"),
	(r"\n*((.+?)\d+:\d+:) error: function cannot return [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* type", "function cannot return some type"),
	(r"\n*((.+?)\d+:\d+:) error: assigning to [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* from incompatible type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*", "assigning to type A from incompatible type B"),
	(r"\n*((.+?)\d+:\d+:) error: subscripted value is not an array\, pointer\, or vector","subscripted value is not an array, pointer, or vector"),
	(r"\n*((.+?)\d+:\d+:) error: parameter name omitted", "parameter name omitted"),
	(r"\n*((.+?)\d+:\d+:) error: passing [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* to parameter of incompatible type", "passing sth to parameter of incompatible type"),
	(r"\n*((.+?)\d+:\d+:) error: invalid argument type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*", "invalid argument type"),
	(r"\n*((.+?)\d+:\d+:) error: incomplete definition of type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*", "incomplete definition of type"),
	(r"\n*((.+?)\d+:\d+:) error: reference to overloaded function could not be resolved", "reference to overloaded function could not be resolved"),
	(r"\n*((.+?)\d+:\d+:) error: called object type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* is not a function or function pointer" ,"called object type 'int' is not a function or function pointer"),
	(r"\n*((.+?)\d+:\d+:) error: duplicate case value",'duplicate case value'),
	(r"\n*((.+?)\d+:\d+:) error: address of overloaded function [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* does not match required type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*", "address of overloaded function 'A' does not match required type 'B'"),
	(r"\n*((.+?)\d+:\d+:) error: attempt to use a poisoned identifier", "attempt to use a poisoned identifier"),
	(r"\n*((.+?)\d+:\d+:) error: indirection requires pointer operand", "indirection requires pointer operand"),
	(r"\n*((.+?)\d+:\d+:) error: operand of type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* is required", "operand of type ? is required"),
	(r"\n*((.+?)\d+:\d+:) error: parameter name omitted", "parameter name omitted"),
	(r"\n*((.+?)\d+:\d+:) error: pointer cannot be cast to type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*", "pointer cannot be cast to type ?"),
	(r"\n*((.+?)\d+:\d+:) error: too few arguments provided to function-like macro invocation", "too few arguments provided to function-like macro invocation"),
	(r"\n*((.+?)\d+:\d+:) error: returning [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* from a function with incompatible result type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*", "returning type A from a function with incompatible result type B"),
	(r"\n*((.+?)\d+:\d+:) error: use of undeclared label [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*", "use of undeclared label"),
	(r"\n*((.+?)\d+:\d+:) error: expected statement", "expected statement"),
	(r"\n*((.+?)\d+:\d+:) error: subscript of pointer to function type", "subscript of pointer to function type"),
	(r"\n*((.+?)\d+:\d+:) error: expected identifier or '\('", "expected identifier or '('"),
	(r"\n*((.+?)\d+:\d+:) error: cannot combine with previous [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* declaration specifier",'cannot combine with previous declaration specifier'),
	(r"\n*((.+?)\d+:\d+:) error: subscript of pointer to incomplete type","subscript of pointer to incomplete type"),
	(r"\n*((.+?)\d+:\d+:) error: statement requires expression of scalar type", "statement requires expression of scalar type"),
	(r"\n*((.+?)\d+:\d+:) error: static declaration of [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* follows non-static declaration", "static declaration of 'A' follows non-static declaration"),
	(r"\n*((.+?):\d+:\d+:) error: use of undeclared identifier '(_OWORD)'\n(\s*?.+?)\n","undeclared identifier OWORD"),
	(r"\n*(.+?):\d+:\d+: error: unknown type name (?:\xe2\x80\x98|')(.*?va_list.*?)(?:\xe2\x80\x99|').*?\n(\s*?.+?)\n","unknown type name va_list"),
	(r"\n*((.+?):\d+:\d+:) error: (\xe2\x80\x98((.+)_\d*)\xe2\x80\x99 undeclared \(first use in this function\)|use of undeclared identifier '((.+?)_\d+)')(?:; did you mean (?:.+?)|)\n  rror: use of undeclared identifier '((?:off|dword|qword|asc|unk)_[0-9,A-F]+|(.+))'.*?\n(\s*?.+?)\n","undeclared identifiers datatypes"),
	(r"\n*((.+?)\d+:\d+:) error: expected \'","expected apostrophe near declaration specifiers"),
	(r"\n*((.+?)\d+:\d+:) error: extraneous \'\)' before","extraneous bracket"),
	(r"\n*((.+?)\d+:\d+:) error: variable has incomplete type 'void'","variable has incomplete type 'void'"),
	(r"\n*((.+?)\d+:\d+:) error: variable has incomplete type","variable has incomplete type"),
	(r"\n*((.+?)\d+:\d+:) error: incompatible integer to pointer conversion assigning","incompatible integer to pointer conversion assigning"),
	(r"\n*((.+?)\d+:\d+:) error: expected function body after function declarator","expected function body after function declarator"),
	(r"\n*((.+?)\d+:\d+:) error: too many arguments to function call","too many arguments to function call"),
	(r"\n*((.+?)\d+:\d+:) error: ISO C requires a named parameter before","ISO C requires a named parameter before"),
	(r"\n*((.+?)\d+:\d+:) error: function cannot return function type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*","function cannot return function type"),
	(r"\n*((.+?)\d+:\d+:) error: unexpected type name [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* expected expression","unexpected type name"),
	(r"\n*((.+?)\d+:\d+:) error: too many arguments provided to function-like macro invocation","too many arguments provided to function-like macro invocation"),
	(r"\n*((.+?)\d+:\d+:) error: a parameter list without types is only allowed in a function definition","a parameter list without types is only allowed in a function definition"),
	(r"\n*((.+?)\d+:\d+:) error: non-object type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* is not assignable","non-object type"),
	(r"\n*((.+?)\d+:\d+:) error: cannot decrement value of type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*","cannot decrement value of type"),
	(r"\n*((.+?)\d+:\d+:) error: array subscript is not an integer","array subscript is not an integer"),
	(r"\n*((.+?)\d+:\d+:) error: statement requires expression of integer type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*", "statement requires expression of integer type"),
	(r"\n*((.+?)\d+:\d+:) error: incompatible pointer to integer conversion assigning to","incompatible pointer to integer conversion assigning to"),
	(r"\n*((.+?)\d+:\d+:) error: offset of incomplete type","offset of incomplete type"),
	(r"\n*((.+?)\d+:\d+:) error: incompatible integer to pointer conversion assigning to","incompatible integer to pointer conversion assigning to"),
	(r"\n*((.+?)\d+:\d+:) error: invalid application of [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* to an incomplete type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*","invalid application of"),
	(r"\n*((.+?)\d+:\d+:) error: non-void function [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* should return a val","non-void function should return a val"),
	(r"\n*((.+?)\d+:\d+:) error: non-void function [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* declared as a function","declared as a function"),
	(r"\n*((.+?)\d+:\d+:) error: invalid conversion between vector type \'\_\_m128d\' (vector of 2 \'double\' values) and integer type 'unsigned long long' of different size","invalid conversion between vector type __m128d"),
	(r"tentative definition has type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* that is never completed","tentative definition has type"),
	(r"\n*((.+?)\d+:\d+:) error: cannot assign to variable [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* with const-qualified type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*","cannot assign to variable"),
	(r"\n*((.+?)\d+:\d+:) error: [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* and [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* (aka [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*) are not pointers to compatible types","not pointers to compatible types"),
	(r"\n*((.+?)\d+:\d+:) error: redefinition of \'\_\_int64\'","redefinition of __int64"),
	(r"\n*((.+?)\d+:\d+:) error: redefinition of \'\_\_int32\'","redefinition of __int32"),
	(r"\n*((.+?)\d+:\d+:) error: redefinition of \'\_\_int16\'","redefinition of __int16"),	
	(r"\n*((.+?)\d+:\d+:) error: redefinition of \'\_\_int8\'","redefinition of __int8"),
	(r"\n*((.+?)\d+:\d+:) error: redefinition of \'\_\_ptr32\'","redefinition of __ptr32"),
	(r"\n*((.+?)\d+:\d+:) error: expression is not assignable","expression is not assignable"),
	(r"\n*((.+?)\d+:\d+:) error: extraneous closing brace \(","extraneous closing brace ("),
	(r"\n*((.+?)\d+:\d+:) error: called object type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\<\:\/]* is not a function or function pointer" ,"called object type '<dependent type>' is not a function or function pointer"),
	(r"\n*((.+?)\d+:\d+:) error: redefinition of \'free\_INSN\_LIST\_list\'","redefinition of free_inst_list"),
	(r"\n*((.+?)\d+:\d+:) error: [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* and [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* are not pointers to compatible types","not pointers to compatible types"),
	(r"\n*((.+?)\d+:\d+:) error: cannot take the address of an rvalue of type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*","cannot take an address of an rvalue of type struct"),
	(r"\n*((.+?)\d+:\d+:) error: cannot assign to non-static data member [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* with const-qualified type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* (aka [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*)","cannot assign to non-static data member with const-qualified type"),
	(r"\n*((.+?)\d+:\d+:) error: \'inline\' can only appear on functions","inline can only appear on functions"),
	(r"\n*((.+?)\d+:\d+:) error: invalid suffix [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]* on integer constant","invalid suffix on integer constant"),
	(r"\n*((.+?)\d+:\d+:) error: invalid [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/\+\=]* at end of declaration\; did you mean [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/\+\=]*\?","invalid A at end of declaration; did you mean B?"),	
	(r"\n*((.+?)\d+:\d+:) error: typedef redefinition with different types \([a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/\+\=]* vs [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/\+\=]* \(aka [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/\+\=]*\)\)","typedef redefinition with different types"),
	(r"\n*((.+?)\d+:\d+:) error: invalid conversion between vector type \'\_\_m128i\'","invalid conversion between vector type __m128i"),
	(r"\n*((.+?)\d+:\d+:) error: invalid conversion between vector type \'\_\_m128d\'","invalid conversion between vector type __m128d"),
	(r"\n*((.+?)\d+:\d+:) error: invalid conversion between vector type \'\_\_m128\'","invalid conversion between vector type __m128"),
	(r"\n*((.+?)\d+:\d+:) error: invalid conversion between vector type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/\+\=]* \(vector of 2 [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/\+\=]* values\) and integer type [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/\+\=]* \(aka [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/\+\=]*\) of different size","invalid conversion between vector types and standard types"),
	(r"\n*((.+?)\d+:\d+:) error: typedef redefinition with different types \([a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/\+\=]* vs [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/\+\=]*\)","typedef redefinition with different types"),
	(r"\n*((.+?)\d+:\d+:) error: redefinition of [a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*","redefinition of a function"),
	(r"\n*((.+?)\d+:\d+:) error: arithmetic on a pointer to an incomplete type \'[a-zA-Z0-9\s\_\[\]\*\(\)\'\,\"\;\&\.\-\>\:\/]*\'","arithmetic on a pointer to an incomplete type")
]



# compare the similarity of compiler error messages at different optimization levels. 
# The code first reads the command line arguments to obtain the project name, 
# then processes specific files and directories to extract and organize error information. 
# By using Edit Distance to calculate the similarity between two strings, 
# the code compares compiler errors at different optimization levels and outputs similarity scores.


# 1. Obtain the project name from command line arguments.
# 2. Define and initialize variables, such as the list of filenames, set of error types, etc.
# 3. Read files from specific directories, extract error types, and their corresponding error information.
# 4. For each error type, iterate through different optimization levels, and create a unique set of functions for each optimization level.
# 5. Create directories to store the results for each error type and optimization level combination.
# 6. Extract error lines and store them as CSV files.
# 7. For each combination of optimization levels, calculate the Edit Distance between error lines and store the scores.
# 8. Write similarity scores and index lists to files for further analysis.





############################################################### main ################################################################
if __name__ == "__main__":
    start_time = time.process_time()
    projname=""
    if len(sys.argv) <= 1:
        print("the arguments are not entered in the command line")
        # return 0
    else:
        for arg in sys.argv:
            print(arg)
        projname = sys.argv[1] 
    ahhh = []
    # for file in os.scandir("/data/Feb_2_2023/gcc_res/original/"):
    nameNumOfFoldersDict = {"gcc":54,"gobmk":54}
    dirnameeTE="/data/"+projname+"TEs/"
    

# 这一部分在
    uniqueErrorType_set = set()
    subList = []
    occ_dir="/data/Feb_2_2023/occurances/"+projname+"/"
    filenamesList = ["cc0","cc1","cc2","cc3","gg0","gg1","gg2","gg3"]
    for fn in filenamesList:
        print("file",fn)
        # if file.endswith(".txt","r"):
        fp = open(occ_dir+fn+".txt","r")
        subDict = {}
        for i, line in enumerate(fp):
            if i >= 2:
                # print("line:",line)
                if ":" in line:
                    print(line)
                    err_key = line[0:line.index(":")]
                    uniqueErrorType_set.add(err_key)
                    subDict[err_key] = line[line.index(":")+1:].rstrip()
                    print("subDict",subDict)
        subList.append(subDict)
    uniqueErrorType_set = sorted(uniqueErrorType_set, key=lambda x: x.lower())
    funcs = []
    funcs = uniqueErrorType_set
    print(len(uniqueErrorType_set))
    

    """uniqueFunc_set 是只每一个func下面，每一对c/g的funcs set
    """
#################################################++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    double_check_funcCount, comparsionCount, double_check_forthisTyErr = 0,0,0
    for errTyNum in range(0,nameNumOfFoldersDict[projname]):  # 54
        # if errTyNum not in [12,13,29,48]:
        if errTyNum not in [7]:
            continue
        print("uniqueErrorType_set[errTyNum]",uniqueErrorType_set[errTyNum])
     # unique_funcs 特指同一ErrTypes下的   
        type_of_coms = ["c","g"]
        for com in type_of_coms:
            fold_dict = {}
            uniqueFunc_set = set() # 每一个 /data/gccTEs/3/g* 或 /data/gccTEs/3/c*
            folders = [com+"0",com+"1",com+"2",com+"3"]
            for comAopt in folders:
                directory = os.fsencode("/data/"+projname+"TEs/"+str(errTyNum)+"/"+comAopt)
                print("directory",directory)
                for file in os.listdir(directory):
                    uniqueFunc_set.add(str(file.decode()))

                # 此时得到属于该ErrorTypeNumber下的所有uniqeFunc
            funcs = []
            funcs = uniqueFunc_set
            print(str(errTyNum)+com, len(uniqueFunc_set))
            
            
            os.system("mkdir -p "+dirnameeTE+str(errTyNum)+"/IndexEachScore")
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

            """生成完毕uniqueFunc_set和uniqueTE，现在把所有error lines排序
            """
 
            # /data/gccTEs/0/c0, c1, c2, c3                
            for idx, comAopt in enumerate(folders):     # 对每一个folder遍历
                fold_array,FUNCLIST = [],[]
                for FUNCFILE in os.listdir(dirnameeTE+str(errTyNum)+"/"+comAopt): # file按照字母顺序排序
                    FUNCLIST.append(FUNCFILE)
                SFUNCLIST = sorted(FUNCLIST, key=lambda x: x.lower())
                double_check_funcCount+=len(SFUNCLIST)
                for FUNCFILE in SFUNCLIST:
                    lines = []
                    print("func_name with this type of error:")
                    print("filename",FUNCFILE)
                    with open(dirnameeTE+str(errTyNum)+"/"+comAopt+"/"+FUNCFILE,"r") as RFUNC:
                        print(dirnameeTE+str(errTyNum)+"/"+comAopt+"/"+FUNCFILE)
                            # 逐行搜索
                        line_marker = -1 # 打开该文件
                        for num, line in enumerate(RFUNC, 0):
                            errorString = uniqueErrorType_set[errTyNum]
                            # print("errorString",errorString)
                            if errorString in line: #TODO 对照pattern修改成tup[0]模式
                                line_marker = num 
                                double_check_forthisTyErr+=1 
                            if line_marker >0 and num == line_marker + 1:  # 读取下面1行
                                fold_array.append(line)       
    
                fold_dict[comAopt] = fold_array
                with open(dirnameeTE+str(errTyNum)+"/"+com+str(idx)+'_lines'+'.csv', 'w') as fp:
                    for item in fold_array:
                        fp.write("%s" % item)     # write each item on a new line
                # for errorTypeStr in funcs:
                #     print("fucccc",errorTypeStr,dirnameeTE+str(errTyNum)+"/"+comAopt)
                #     #TODO: 需要替代 这个for loop只是为了找到match func
                #     grepPattern = ""
                #     for tup in patterns: # each error type, iterate through all patterns
                #         if tup[1] == errorTypeStr: 
                #             # print("tup[0]",tup[0])
                #             grepPattern = tup[0][tup[0].find("error:"):len(tup[0])]
                #             print("grepPattern",grepPattern)
                #             res=subprocess.run(["grep", "\"", grepPattern,  "\"", dirnameeTE+str(errTyNum)+"/"+comAopt, "-P"], stdout=subprocess.PIPE)
                #             print("res.stdout.decode('utf-8')",res.stdout.decode('utf-8'))
                #             if res.stdout.decode('utf-8'): # contains errors
                #                 resList = res.stdout.decode('utf-8').split("\n")[:-1] # list最后一个元素为空，所以去掉
                #             # oj = findf(grepPattern, dirnameeTE+str(errTyNum)+"/"+comAopt)
                #             # if (type(oj) != type(None)):
                #                 if len(resList) != 0:
                #                     ftcs.append(resList)


                # print("len(ftcs)",len(ftcs))

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++ c1_lines +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            
            
            
           
            print("fold_dict",fold_dict)
            # opt_level = -1
           
            for opt_level in range(1,4): # 1-3, （4不包括）
                scores_arr,index_list = [],[]
                sim_score_count = 0
                if not (com+str(opt_level) in fold_dict and com+str(opt_level-1) in fold_dict):
                    continue 
                # outer
                for o_idx,outer_line in enumerate(fold_dict[com+str(opt_level)]):  # O1,O2,O3 +1 compare obtained outerline with every line in respective forms
                    max_simi = 0
                    # double_check_forthisTyErr+=1
                    i_arr = [] # funcs, error_lines for inner comparsion
                    # inner
                    for i_index, inner_line in enumerate(fold_dict[com+str(opt_level-1)]): # O0,O1,O2
                        sim_score_count += 1
                        # 打印出O1,O0,inner_index,sim_score_count
                        # print(com+str(opt_level),com+str(opt_level-1),"inner_index",str(i_index),"sim_score_count",sim_score_count)
                        outer_line = outer_line.rstrip() # remove \n
                        inner_line = inner_line.rstrip() # remove \n
                        # print("outer_line",outer_line)
                        # print("inner_line",inner_line)
                        simScore = EditDistance(outer_line,inner_line)
                        # print("This simScore:",simScore)
                        if simScore > max_simi:
                            i_arr = []
                            i_arr.append(i_index)
                            max_simi = simScore
                            # print("max_simi",max_simi)
                        elif max_simi > 0 and simScore == max_simi:
                            i_arr.append(i_index)
                
                    scores_arr.append(max_simi)
                    index_list.append(i_arr)
                    print("Err"+str(errTyNum)+" {"+com+str(opt_level)+" vs "+com+str(opt_level-1)+"}","line_num:"+str(o_idx),"Time elapsed:",time.process_time()-start_time,"max_simi",max_simi,)        
                    comparsionCount+=1

                print("+++++++++++ scores_arr ++++++++")
                print(scores_arr)

                with open(dirnameeTE+str(errTyNum)+'/score_'+com+str(opt_level)+'.txt', 'w') as fp:
                    for item in scores_arr:
                        # write each item on a new line
                        fp.write("%s\n" % item)

                with open(dirnameeTE+str(errTyNum)+'/IndexEachScore/index_arr_'+com+str(opt_level)+'.txt', 'w') as fp:
                    for item in index_list:
                        # write each item on a new line
                        fp.write("%s\n" % item)
                        
            print("double_check_forthisTyErr",double_check_forthisTyErr,"comparsionCount",comparsionCount,"double_check_funcCount",double_check_funcCount)


