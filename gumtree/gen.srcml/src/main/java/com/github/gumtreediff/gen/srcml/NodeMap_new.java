package com.github.gumtreediff.gen.srcml;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.stream.Collectors;

public class NodeMap_new {



    public static Map<Integer, String> map;
    public static Map<Integer, String> StatementMap;
    public static Map<Integer, String> DeclarationMap;


        static {
            map = new HashMap<Integer, String>();
            map.put(0,"unit");
            map.put(    1   , "comment:block");
            map.put(    2   , "comment:line");
            map.put(    6   , "literal:string");
            map.put(    7   , "literal:char");
            map.put(    8   , "literal:number");
            map.put(    9   , "literal:boolean");
            map.put(    10  , "literal:null");
            map.put(    11  , "literal:complex");
            map.put(    12  , "operator");
            map.put(    13  , "modifier");
            map.put(    14  , "name");
            map.put(    16  , "type");
            map.put(    17  , "type:prev");
            map.put(    19  , "block");
            map.put(    20  , "block_content");
            map.put(    21  , "block:pseudo");
            map.put(    22  , "index");
            map.put(    23  , "decltype");
            map.put(    24  , "typename");
            map.put(    25  , "atomic");
            map.put(    26  , "assert:static");
            map.put(    27  , "generic_selection");
            map.put(    28  , "selector");
            map.put(    29  , "association_list");
            map.put(    30  , "association");
            map.put(    31  , "expr_stmt");
            map.put(    32  , "expr");
            map.put(    33  , "decl_stmt");
            map.put(    34  , "decl");
            map.put(    35  , "init");
            map.put(    36  , "range");
            map.put(    37  , "break");
            map.put(    38  , "continue");
            map.put(    39  , "goto");
            map.put(    40  , "label");
            map.put(    41  , "typedef");
            map.put(    42  , "asm");
            map.put(    43  , "macro");
            map.put(    44  , "enum");
            map.put(    45  , "enum_decl");
            map.put(    46  , "if_stmt");
            map.put(    47  , "if");
            map.put(    48  , "ternary");
            map.put(    49  , "then");
            map.put(    50  , "else");
            map.put(    51  , "if:elseif");
            map.put(    52  , "while");
            map.put(    53  , "typeof");
            map.put(    54  , "do");
            map.put(    55  , "switch");
            map.put(    56  , "case");
            map.put(    57  , "default");
            map.put(    58  , "for");
            map.put(    59  , "foreach");
            map.put(    60  , "control");
            map.put(    62  , "condition");
            map.put(    63  , "incr");
            map.put(    65  , "function");
            map.put(    66  , "function_decl");
            map.put(    67  , "lambda");
            map.put(    68  , "specifier");
            map.put(    69  , "return");
            map.put(    70  , "call");
            map.put(    71  , "sizeof");
            map.put(    72  , "parameter_list");
            map.put(    73  , "parameter");
            map.put(    74  , "krparameter_list");
            map.put(    75  , "krparameter");
            map.put(    76  , "argument_list");
            map.put(    77  , "argument");
            map.put(    78  , "capture");
            map.put(    79  , "parameter_list:pseudo");
            map.put(    80  , "parameter_list:indexer");
            map.put(    81  , "struct");
            map.put(    82  , "struct_decl");
            map.put(    83  , "union");
            map.put(    84  , "union_decl");
            map.put(    85  , "class");
            map.put(    86  , "class_decl");
            map.put(    87  , "public");
            map.put(    88  , "public:default");
            map.put(    89  , "private");
            map.put(    90  , "private:default");
            map.put(    91  , "protected");
            map.put(    92  , "protected:default");
            map.put(    93  , "signals");
            map.put(    94  , "forever");
            map.put(    95  , "emit");
            map.put(    96  , "member_init_list");
            map.put(    98  , "constructor");
            map.put(    99  , "constructor_decl");
            map.put(    100 , "destructor");
            map.put(    101 , "destructor_decl");
            map.put(    102 , "super_list");
            map.put(    103 , "super");
            map.put(    104 , "friend");
            map.put(    106 , "extern");
            map.put(    107 , "namespace");
            map.put(    108 , "using");
            map.put(    109 , "try");
            map.put(    110 , "catch");
            map.put(    111 , "finally");
            map.put(    112 , "throw");
            map.put(    114 , "throws");
            map.put(    115 , "noexcept");
            map.put(    116 , "template");
            map.put(    118 , "argument_list:generic");
            map.put(    122 , "parameter_list:generic");
            map.put(    123 , "directive");
            map.put(    124 , "file");
            map.put(    125 , "number");
            map.put(    126 , "literal");
            map.put(    127 , "include");
            map.put(    128 , "define");
            map.put(    129 , "undef");
            map.put(    130 , "line");
            map.put(    131 , "cpp:if");
            map.put(    132 , "ifdef");
            map.put(    133 , "ifndef");
            map.put(    134 , "cpp:else");
            map.put(    135 , "elif");
            map.put(    136 , "endif");
            map.put(    137 , "cpp:then");
            map.put(    138 , "pragma");
            map.put(    139 , "error");
            map.put(    140 , "warning");
            map.put(    142 , "value");
            map.put(    143 , "empty");
            map.put(    144 , "marker");
            map.put(    145 , "region");
            map.put(    146 , "endregion");
            map.put(    147 , "import");
            map.put(    149 , "parse");
            map.put(    150 , "mode");
            map.put(    151 , "lock");
            map.put(    152 , "fixed");
            map.put(    153 , "checked");
            map.put(    154 , "unchecked");
            map.put(    155 , "unsafe");
            map.put(    156 , "using_stmt");
            map.put(    157 , "delegate");
            map.put(    158 , "event");
            map.put(    159 , "constraint");
            map.put(    160 , "extends");
            map.put(    161 , "implements");
            map.put(    163 , "package");
            map.put(    164 , "assert");
            map.put(    165 , "synchronized");
            map.put(    166 , "interface");
            map.put(    167 , "interface_decl");
            map.put(    168 , "annotation_defn");
            map.put(    169 , "static");
            map.put(    170 , "attribute");
            map.put(    171 , "target");
            map.put(    172 , "linq");
            map.put(    173 , "from");
            map.put(    174 , "select");
            map.put(    175 , "where");
            map.put(    176 , "let");
            map.put(    177 , "orderby");
            map.put(    178 , "group");
            map.put(    179 , "join");
            map.put(    180 , "in");
            map.put(    181 , "on");
            map.put(    182 , "equals");
            map.put(    183 , "by");
            map.put(    184 , "into");
            map.put(    185 , "escape");
            map.put(    186 , "annotation");
            map.put(    187 , "alignas");
            map.put(    188 , "alignof");
            map.put(    189 , "typeid");
            map.put(    190 , "sizeof:pack");
            map.put(    191 , "enum:class");
            map.put(    192 , "enum_decl:class");
            map.put(    193 , "function:operator");
            map.put(    194 , "function_decl:operator");
            map.put(    195 , "ref_qualifier");
            map.put(    196 , "receiver");
            map.put(    197 , "message");
            map.put(    199 , "protocol_list");
            map.put(    200 , "category");

//
//            map.put(1	,	"unit");
//            map.put(2	,	"comment");
//            map.put(3	,	"literal");
//            map.put(4	,	"operator");
//            map.put(5	,	"modifier");
//            map.put(6	,	"name");
//            map.put(7	,	"type");
//            map.put(8	,	"condition");
//            map.put(9	,	"block");
//            map.put(10	,	"index");
//            map.put(11	,	"decltype");
//            map.put(12	,	"typename");
//            map.put(13	,	"atomic");
//            map.put(14	,	"assert");
//            map.put(15	,	"generic_selection");
//            map.put(16	,	"selector");
//            map.put(17	,	"association_list");
//            map.put(18	,	"association");
//            map.put(19	,	"expr_stmt");
//            map.put(20	,	"expr");
//            map.put(21	,	"decl_stmt");
//            map.put(22	,	"decl");
//            map.put(23	,	"init");
//            map.put(24	,	"range");
//            map.put(25	,	"break");
//            map.put(26	,	"continue");
//            map.put(27	,	"goto");
//            map.put(28	,	"label");
//            map.put(29	,	"typedef");
//            map.put(30	,	"asm");
//            map.put(31	,	"macro");
//            map.put(32	,	"enum");
//            map.put(33	,	"enum_decl");
//            map.put(34	,	"if");
//            map.put(35	,	"ternary");
//            map.put(36	,	"then");
//            map.put(37	,	"else");
//            map.put(38	,	"elseif");
//            map.put(39	,	"while");
//            map.put(40	,	"typeof");
//            map.put(41	,	"do");
//            map.put(42	,	"switch");
//            map.put(43	,	"case");
//            map.put(44	,	"default");
//            map.put(45	,	"for");
//            map.put(46	,	"foreach");
//            map.put(47	,	"control");
//            map.put(48	,	"incr");
//            map.put(49	,	"function");
//            map.put(50	,	"function_decl");
//            map.put(51	,	"lambda");
//            map.put(52	,	"specifier");
//            map.put(53	,	"return");
//            map.put(54	,	"call");
//            map.put(55	,	"sizeof");
//            map.put(56	,	"parameter_list");
//            map.put(57	,	"parameter");
//            map.put(58	,	"krparameter_list");
//            map.put(59	,	"krparameter");
//            map.put(60	,	"argument_list");
//            map.put(61	,	"argument");
//            map.put(62	,	"capture");
//            map.put(63	,	"struct");
//            map.put(64	,	"struct_decl");
//            map.put(65	,	"union");
//            map.put(66	,	"union_decl");
//            map.put(67	,	"class");
//            map.put(68	,	"class_decl");
//            map.put(69	,	"public");
//            map.put(70	,	"private");
//            map.put(71	,	"protected");
//            map.put(72	,	"signals");
//            map.put(73	,	"forever");
//            map.put(74	,	"emit");
//            map.put(75	,	"member_init_list");
//            map.put(76	,	"constructor");
//            map.put(77	,	"constructor_decl");
//            map.put(78	,	"destructor");
//            map.put(79	,	"destructor_decl");
//            map.put(80	,	"super");
//            map.put(81	,	"friend");
//            map.put(82	,	"extern");
//            map.put(83	,	"namespace");
//            map.put(84	,	"using");
//            map.put(85	,	"try");
//            map.put(86	,	"catch");
//            map.put(87	,	"finally");
//            map.put(88	,	"throw");
//            map.put(89	,	"throws");
//            map.put(90	,	"noexcept");
//            map.put(91	,	"template");
//            map.put(92	,	"directive");
//            map.put(93	,	"file");
//            map.put(94	,	"number");
//            map.put(95	,	"include");
//            map.put(96	,	"define");
//            map.put(97	,	"undef");
//            map.put(98	,	"line");
//            map.put(99	,	"ifdef");
//            map.put(100	,	"ifndef");
//            map.put(101	,	"elif");
//            map.put(102	,	"endif");
//            map.put(103	,	"pragma");
//            map.put(104	,	"error");
//            map.put(105	,	"warning");
//            map.put(106	,	"value");
//            map.put(107	,	"empty");
//            map.put(108	,	"region");
//            map.put(109	,	"endregion");
//            map.put(110	,	"import");
//            map.put(111	,	"marker");
//            map.put(112	,	"parse");
//            map.put(113	,	"mode");
//            map.put(114	,	"lock");
//            map.put(115	,	"fixed");
//            map.put(116	,	"checked");
//            map.put(117	,	"unchecked");
//            map.put(118	,	"unsafe");
//            map.put(119	,	"using_stmt");
//            map.put(120	,	"delegate");
//            map.put(121	,	"event");
//            map.put(122	,	"constraint");
//            map.put(123	,	"extends");
//            map.put(124	,	"implements");
//            map.put(125	,	"package");
//            map.put(126	,	"synchronized");
//            map.put(127	,	"interface");
//            map.put(128	,	"interface_decl");
//            map.put(129	,	"annotation_defn");
//            map.put(130	,	"static");
//            map.put(131	,	"attribute");
//            map.put(132	,	"target");
//            map.put(133	,	"linq");
//            map.put(134	,	"from");
//            map.put(135	,	"select");
//            map.put(136	,	"where");
//            map.put(137	,	"let");
//            map.put(138	,	"orderby");
//            map.put(139	,	"group");
//            map.put(140	,	"join");
//            map.put(141	,	"in");
//            map.put(142	,	"on");
//            map.put(143	,	"equals");
//            map.put(144	,	"by");
//            map.put(145	,	"into");
//            map.put(146	,	"escape");
//            map.put(147	,	"annotation");
//            map.put(148	,	"alignas");
//            map.put(149	,	"alignof");
//            map.put(150	,	"typeid");
//            map.put(151	,	"ref_qualifier");
//            map.put(152	,	"receiver");
//            map.put(153	,	"message");
//            map.put(154	,	"protocol_list");
//            map.put(155	,	"category");
//            map.put(156	,	"protocol");
//            map.put(157	,	"required");
//            map.put(158	,	"optional");
//            map.put(159	,	"property");
//            map.put(160	,	"attribute_list");
//            map.put(161	,	"synthesize");
//            map.put(162	,	"dynamic");
//            map.put(163	,	"encode");
//            map.put(164	,	"autoreleasepool");
//            map.put(165	,	"compatibility_alias");
//            map.put(166	,	"protocol_decl");
//            map.put(167	,	"cast");
//            map.put(168	,	"position");
//            map.put(169	,	"clause");
//            map.put(170	,	"empty_stmt");
//            map.put(171	,	"cpp:if");
//            map.put(172	,	"cpp:else");
//            map.put(173	,	"literal:string");
//            map.put(174	,	"literal:number");
//            map.put(175	,	"literal:char");
//            map.put(176	,	"literal:boolean");
//            map.put(177	,	"literal:complex");
//            map.put(178	,	"literal:null");



        }

    static {
        DeclarationMap = new HashMap<Integer, String>();
        DeclarationMap.put(21  ,       "decl_stmt");
        DeclarationMap.put(22  ,       "decl");
        DeclarationMap.put(50  ,       "function_decl");
        DeclarationMap.put(49  ,       "function");
        DeclarationMap.put(5   ,       "modifier");
        DeclarationMap.put(29  ,       "typedef");
        DeclarationMap.put(23  ,       "init");
        DeclarationMap.put(24  ,       "range");
        DeclarationMap.put(64  ,       "struct_decl");
        DeclarationMap.put(63  ,       "struct");
        DeclarationMap.put(65  ,       "union");
        DeclarationMap.put(66  ,       "union_decl");
        DeclarationMap.put(32  ,       "enum");
        DeclarationMap.put(33  ,       "enum_decl");
    }
    static {
        StatementMap = new HashMap<Integer, String>();

        StatementMap.put(    46  , "if_stmt");

        StatementMap.put(    52  , "while");
        StatementMap.put(    26  , "assert:static");
        StatementMap.put(    164 , "assert");
        StatementMap.put(    31  , "expr_stmt");
        StatementMap.put(    33  , "decl_stmt");
        StatementMap.put(    54  , "do");
        StatementMap.put(    58  , "for");
        StatementMap.put(    59  , "foreach");
        StatementMap.put(    69  , "return");
        StatementMap.put(    37  , "break");
        StatementMap.put(    38  , "continue");
        StatementMap.put(    39  , "goto");
        StatementMap.put(    40  , "label");

        StatementMap.put(    43  , "macro");
        StatementMap.put(    55  , "switch");

        StatementMap.put(    81  , "struct");
        StatementMap.put(    82  , "struct_decl");
        StatementMap.put(    83  , "union");
        StatementMap.put(    84  , "union_decl");
        StatementMap.put(    85  , "class");
        StatementMap.put(    86  , "class_decl");
        StatementMap.put(    44  , "enum");
        StatementMap.put(    45  , "enum_decl");
        StatementMap.put(    65  , "function");
        StatementMap.put(    66  , "function_decl");
//        StatementMap.put(34	,	"if");
////        StatementMap.put(8	,	"condition");
//        StatementMap.put(36	,	"then");
//        StatementMap.put(37	,	"else");
//        StatementMap.put(38	,	"elseif");
//        StatementMap.put(39	,	"while");
//        StatementMap.put(45	,	"for");
//        StatementMap.put(41	,	"do");
////        StatementMap.put(25	,	"break");
////        StatementMap.put(26	,	"continue");
//        StatementMap.put(53	,	"return");
//        StatementMap.put(42	,	"switch");
////        StatementMap.put(43	,	"case");
////        StatementMap.put(44	,	"default");
//        StatementMap.put(9	,	"block");
//        StatementMap.put(27	,	"goto");
//        StatementMap.put(28	,	"label");
//
//        StatementMap.put(21	,	"decl_stmt");
////        StatementMap.put(22	,	"decl");
//        StatementMap.put(50	,	"function_decl");
//        StatementMap.put(49	,	"function");
////        StatementMap.put(5	,	"modifier");
//        StatementMap.put(29	,	"typedef");
////        StatementMap.put(23	,	"init");
////        StatementMap.put(24	,	"range");
//        StatementMap.put(64	,	"struct_decl");
//        StatementMap.put(63	,	"struct");
//        StatementMap.put(65	,	"union");
//        StatementMap.put(66	,	"union_decl");
//        StatementMap.put(32	,	"enum");
//        StatementMap.put(33	,	"enum_decl");
//        StatementMap.put(19	,	"expr_stmt");
//        StatementMap.put(82	,	"extern");
////        StatementMap.put(31	,	"macro");
    }
//    static {
//        StatementMap = new HashMap<Integer, String>();
//
//        StatementMap.put(9	,	"block");
//        StatementMap.put(14	,	"assert");
//        StatementMap.put(15	,	"generic_selection");
//        StatementMap.put(16	,	"selector");
//        StatementMap.put(17	,	"association_list");
//        StatementMap.put(18	,	"association");
//        StatementMap.put(19	,	"expr_stmt");
////        StatementMap.put(20	,	"expr");
//        StatementMap.put(21	,	"decl_stmt");
//        StatementMap.put(22	,	"decl");
//        StatementMap.put(23	,	"init");
//        StatementMap.put(24	,	"range");
//        StatementMap.put(25	,	"break");
//        StatementMap.put(26	,	"continue");
//        StatementMap.put(27	,	"goto");
//        StatementMap.put(28	,	"label");
//        StatementMap.put(29	,	"typedef");
//        StatementMap.put(30	,	"asm");
//        StatementMap.put(31	,	"macro");
//        StatementMap.put(32	,	"enum");
//        StatementMap.put(33	,	"enum_decl");
//        StatementMap.put(34	,	"if");
//        StatementMap.put(35	,	"ternary");
//        StatementMap.put(36	,	"then");
//        StatementMap.put(37	,	"else");
//        StatementMap.put(38	,	"elseif");
//        StatementMap.put(39	,	"while");
//        StatementMap.put(40	,	"typeof");
//        StatementMap.put(41	,	"do");
//        StatementMap.put(42	,	"switch");
//        StatementMap.put(43	,	"case");
//        StatementMap.put(44	,	"default");
//        StatementMap.put(45	,	"for");
//        StatementMap.put(46	,	"foreach");
//        StatementMap.put(47	,	"control");
//
//        StatementMap.put(49	,	"function");
//        StatementMap.put(50	,	"function_decl");
//        StatementMap.put(53	,	"return");
//
//        StatementMap.put(63	,	"struct");
//        StatementMap.put(64	,	"struct_decl");
//        StatementMap.put(65	,	"union");
//        StatementMap.put(66	,	"union_decl");
//        StatementMap.put(67	,	"class");
//        StatementMap.put(68	,	"class_decl");
//
//        StatementMap.put(73	,	"forever");
//        StatementMap.put(74	,	"emit");
//        StatementMap.put(88	,	"throw");
//
//        StatementMap.put(95	,	"include");
//        StatementMap.put(96	,	"define");
//
//        StatementMap.put(114	,	"lock");
//        StatementMap.put(115	,	"fixed");
//        StatementMap.put(116	,	"checked");
//        StatementMap.put(117	,	"unchecked");
//        StatementMap.put(118	,	"unsafe");
//        StatementMap.put(119	,	"using_stmt");
//
////        StatementMap.put(14	,"assert");
////        StatementMap.put(16	,"expr_stmt");
////        StatementMap.put(18	,"decl_stmt");
////        StatementMap.put(19	,"decl");
////        StatementMap.put(21	,"break");
////        StatementMap.put(22	,"continue");
////        StatementMap.put(23	,"goto");
////        StatementMap.put(24	,"label");
////        StatementMap.put(25	,"typedef");
//////        StatementMap.put(26	,"asm");
////        StatementMap.put(27	,"enum");
////        StatementMap.put(30	,"while");
////        StatementMap.put(31	,"lock");
////        StatementMap.put(32	,"fixed");
////        StatementMap.put(33	,"checked");
////        StatementMap.put(34	,"unchecked");
////        StatementMap.put(35	,"unsafe");
////        StatementMap.put(36	,"do");
////        StatementMap.put(37	,"switch");
////        StatementMap.put(38	,"case");
////        StatementMap.put(39	,"default");
////        StatementMap.put(40	,"for");
////        StatementMap.put(41	,"foreach");
////        StatementMap.put(45	,"function");
////        StatementMap.put(46	,"function_decl");
////        StatementMap.put(49	,"return");
////        StatementMap.put(59	,"struct");
////        StatementMap.put(60	,"struct_decl");
////        StatementMap.put(61	,"union");
////        StatementMap.put(62	,"union_decl");
////        StatementMap.put(63	,"class");
////        StatementMap.put(64	,"class_decl");
////        StatementMap.put(70	,"try");
////        StatementMap.put(71	,"catch");
////        StatementMap.put(72	,"finally");
////        StatementMap.put(73	,"throw");
////        StatementMap.put(74	,"throws");
////        StatementMap.put(80	,"include");
////        StatementMap.put(81	,"define");
////        StatementMap.put(82	,"undef");
////        StatementMap.put(84	,"if");
////        StatementMap.put(85	,"ifdef");
////        StatementMap.put(86	,"ifndef");
////        StatementMap.put(87	,"else");
////        StatementMap.put(88	,"elif");
////        StatementMap.put(89	,"endif");
////        StatementMap.put(90	,"then");
////        StatementMap.put(91	,"pragma");
////        StatementMap.put(92	,"error");
////        StatementMap.put(93	,"macro");
////        StatementMap.put(96	,"constructor_decl");
//
//
//
//    }

    public static <T, E> List<T> getKeysByValue(Map<T, E> map, E value) {
        return map.entrySet()
                .stream()
                .filter(entry -> Objects.equals(entry.getValue(), value))
                .map(Map.Entry::getKey)
                .collect(Collectors.toList());
    }

}
