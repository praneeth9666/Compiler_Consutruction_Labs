from typing import List, Dict


class Int:
    def __init__(self, value):
        self.value = value


class Bool:
    def __init__(self, value):
        self.value = value


class Big:
    def __init__(self, value):
        self.value = value


def is_int(val):
    return isinstance(val.value, int)


def is_bool(val):
    return isinstance(val.value, bool)


def is_big(val):
    return isinstance(val.value, object)


def inject_int(val: int):
    return Int(val)


def inject_bool(val: bool):
    return Bool(val)


def inject_big(val: object):
    return Big(val)


def project_int(val):
    if not is_int(val):
        raise Exception("Type Error")
    return val.value


def project_bool(val):
    if not is_bool(val):
        raise Exception("Type Error")
    return val.value


def project_big(val):
    if not is_big(val):
        raise Exception("Type Error")
    return val.value


def error_pyobj(val):
    raise Exception(val)


def is_true(val):
    if isinstance(val, Int):
        return val.value != 0
    elif isinstance(val, Bool):
        return val.value
    elif isinstance(val, Big):
        if isinstance(val, List) or isinstance(val, Dict):
            return len(val.value) != 0
        return val.value != 0


def not_equal(val1, val2):
    return val1.value != val2.value


def equal(val1, val2):
    return val1.value == val2.value


def add(val1, val2):
    return val1.value + val2.value


def print_any(val):
    print(val.value)


x = inject_int(5)
y = inject_int(10)
z = inject_int(0)
temp32 = inject_int(0)
temp3 = is_int(x)
if temp3:
    temp2 = is_int(temp32)
else:
    temp2 = is_int(x)

temp5 = temp2
if temp5:

    temp6 = project_int(x)
    temp7 = project_int(temp32)
    temp6 = temp6 != temp7
    temp1 = inject_bool(temp6)
else:
    temp9 = is_bool(x)
    if temp9:
        temp8 = is_bool(temp32)
    else:
        temp8 = is_bool(x)

    temp11 = temp8
    if temp11:

        temp12 = project_bool(x)
        temp13 = project_bool(temp32)
        temp12 = temp12 != temp13
        temp1 = inject_bool(temp12)
    else:
        temp15 = is_int(x)
        if temp15:
            temp14 = is_bool(temp32)
        else:
            temp14 = is_int(x)

        temp17 = temp14
        if temp17:

            temp18 = project_int(x)
            temp19 = project_bool(temp32)
            temp18 = temp18 != temp19
            temp1 = inject_bool(temp18)
        else:
            temp21 = is_bool(x)
            if temp21:
                temp20 = is_int(temp32)
            else:
                temp20 = is_bool(x)

            temp23 = temp20
            if temp23:

                temp24 = project_bool(x)
                temp25 = project_int(temp32)
                temp24 = temp24 != temp25
                temp1 = inject_bool(temp24)
            else:
                temp27 = is_big(x)
                if temp27:
                    temp26 = is_big(temp32)
                else:
                    temp26 = is_big(x)

                temp29 = temp26
                if temp29:

                    temp30 = project_big(x)
                    temp31 = project_big(temp32)
                    temp30 = not_equal(temp30, temp31)
                    temp1 = inject_bool(temp30)
                else:
                    error_pyobj("Type Checking Error")

temp0 = temp1
temp34 = is_int(temp0)
if temp34:
    temp0 = project_int(temp0)
else:
    temp35 = is_bool(temp0)
    if temp35:
        temp0 = project_bool(temp0)
    else:
        temp36 = is_big(temp0)
        if temp36:
            temp0 = project_big(temp0)
        else:
            error_pyobj("Type Checking Error")
temp33 = inject_int(temp0)
temp595 = is_true(temp33)
while temp595:
    temp38 = inject_int(1)
    temp39 = is_int(temp38)
    if temp39:
        temp38 = project_int(temp38)
        temp38 = -temp38
        temp38 = inject_int(temp38)
    else:
        temp40 = is_bool(temp38)
        if temp40:
            temp38 = project_bool(temp38)
            temp38 = -temp38
            temp38 = inject_bool(temp38)
        else:
            temp41 = is_big(temp38)
            if temp41:
                temp38 = project_big(temp38)
                temp38 = -temp38
                temp38 = inject_big(temp38)
            else:
                error_pyobj("Type Checking Error")
    temp44 = is_int(x)
    if temp44:
        temp43 = is_int(temp38)
    else:
        temp43 = is_int(x)

    temp46 = temp43
    if temp46:

        temp48 = project_int(x)
        temp49 = project_int(temp38)
        temp47 = temp48 + temp49
        temp42 = inject_int(temp47)
    else:
        temp51 = is_bool(x)
        if temp51:
            temp50 = is_bool(temp38)
        else:
            temp50 = is_bool(x)

        temp53 = temp50
        if temp53:

            temp55 = project_bool(x)
            temp56 = project_bool(temp38)
            temp54 = temp55 + temp56
            temp42 = inject_bool(temp54)
        else:
            temp58 = is_bool(x)
            if temp58:
                temp57 = is_int(temp38)
            else:
                temp57 = is_bool(x)

            temp60 = temp57
            if temp60:

                temp62 = project_bool(x)
                temp63 = project_int(temp38)
                temp61 = temp62 + temp63
                temp42 = inject_int(temp61)
            else:
                temp65 = is_int(x)
                if temp65:
                    temp64 = is_bool(temp38)
                else:
                    temp64 = is_int(x)

                temp67 = temp64
                if temp67:

                    temp69 = project_int(x)
                    temp70 = project_bool(temp38)
                    temp68 = temp69 + temp70
                    temp42 = inject_int(temp68)
                else:
                    temp72 = is_big(x)
                    if temp72:
                        temp71 = is_big(temp38)
                    else:
                        temp71 = is_big(x)

                    temp74 = temp71
                    if temp74:

                        temp75 = project_big(x)
                        temp76 = project_big(temp38)
                        temp77 = add(temp75, temp76)
                        temp42 = inject_big(temp77)
                    else:
                        error_pyobj("Type Checking Error")

    x = temp42
    y_copy = y
    inner_loop_done = inject_int(0)
    temp110 = inject_int(0)
    temp81 = is_int(y_copy)
    if temp81:
        temp80 = is_int(temp110)
    else:
        temp80 = is_int(y_copy)

    temp83 = temp80
    if temp83:

        temp84 = project_int(y_copy)
        temp85 = project_int(temp110)
        temp84 = temp84 != temp85
        temp79 = inject_bool(temp84)
    else:
        temp87 = is_bool(y_copy)
        if temp87:
            temp86 = is_bool(temp110)
        else:
            temp86 = is_bool(y_copy)

        temp89 = temp86
        if temp89:

            temp90 = project_bool(y_copy)
            temp91 = project_bool(temp110)
            temp90 = temp90 != temp91
            temp79 = inject_bool(temp90)
        else:
            temp93 = is_int(y_copy)
            if temp93:
                temp92 = is_bool(temp110)
            else:
                temp92 = is_int(y_copy)

            temp95 = temp92
            if temp95:

                temp96 = project_int(y_copy)
                temp97 = project_bool(temp110)
                temp96 = temp96 != temp97
                temp79 = inject_bool(temp96)
            else:
                temp99 = is_bool(y_copy)
                if temp99:
                    temp98 = is_int(temp110)
                else:
                    temp98 = is_bool(y_copy)

                temp101 = temp98
                if temp101:

                    temp102 = project_bool(y_copy)
                    temp103 = project_int(temp110)
                    temp102 = temp102 != temp103
                    temp79 = inject_bool(temp102)
                else:
                    temp105 = is_big(y_copy)
                    if temp105:
                        temp104 = is_big(temp110)
                    else:
                        temp104 = is_big(y_copy)

                    temp107 = temp104
                    if temp107:

                        temp108 = project_big(y_copy)
                        temp109 = project_big(temp110)
                        temp108 = not_equal(temp108, temp109)
                        temp79 = inject_bool(temp108)
                    else:
                        error_pyobj("Type Checking Error")

    temp78 = temp79
    temp112 = is_int(temp78)
    if temp112:
        temp78 = project_int(temp78)
    else:
        temp113 = is_bool(temp78)
        if temp113:
            temp78 = project_bool(temp78)
        else:
            temp114 = is_big(temp78)
            if temp114:
                temp78 = project_big(temp78)
            else:
                error_pyobj("Type Checking Error")
    temp111 = inject_int(temp78)
    temp117 = inner_loop_done
    temp118 = is_true(temp117)
    if temp118:
        temp116 = inject_bool(False)
    else:
        temp116 = inject_bool(True)
    temp115 = temp116
    temp120 = is_int(temp115)
    if temp120:
        temp115 = project_int(temp115)
    else:
        temp121 = is_bool(temp115)
        if temp121:
            temp115 = project_bool(temp115)
        else:
            temp122 = is_big(temp115)
            if temp122:
                temp115 = project_big(temp115)
            else:
                error_pyobj("Type Checking Error")
    temp119 = inject_int(temp115)
    temp124 = temp111
    temp125 = is_true(temp124)
    if temp125:
        temp123 = temp119
    else:
        temp123 = temp111
    temp585 = is_true(temp123)
    while temp585:
        temp127 = inject_int(1)
        temp128 = is_int(temp127)
        if temp128:
            temp127 = project_int(temp127)
            temp127 = -temp127
            temp127 = inject_int(temp127)
        else:
            temp129 = is_bool(temp127)
            if temp129:
                temp127 = project_bool(temp127)
                temp127 = -temp127
                temp127 = inject_bool(temp127)
            else:
                temp130 = is_big(temp127)
                if temp130:
                    temp127 = project_big(temp127)
                    temp127 = -temp127
                    temp127 = inject_big(temp127)
                else:
                    error_pyobj("Type Checking Error")
        temp133 = is_int(y_copy)
        if temp133:
            temp132 = is_int(temp127)
        else:
            temp132 = is_int(y_copy)

        temp135 = temp132
        if temp135:

            temp137 = project_int(y_copy)
            temp138 = project_int(temp127)
            temp136 = temp137 + temp138
            temp131 = inject_int(temp136)
        else:
            temp140 = is_bool(y_copy)
            if temp140:
                temp139 = is_bool(temp127)
            else:
                temp139 = is_bool(y_copy)

            temp142 = temp139
            if temp142:

                temp144 = project_bool(y_copy)
                temp145 = project_bool(temp127)
                temp143 = temp144 + temp145
                temp131 = inject_bool(temp143)
            else:
                temp147 = is_bool(y_copy)
                if temp147:
                    temp146 = is_int(temp127)
                else:
                    temp146 = is_bool(y_copy)

                temp149 = temp146
                if temp149:

                    temp151 = project_bool(y_copy)
                    temp152 = project_int(temp127)
                    temp150 = temp151 + temp152
                    temp131 = inject_int(temp150)
                else:
                    temp154 = is_int(y_copy)
                    if temp154:
                        temp153 = is_bool(temp127)
                    else:
                        temp153 = is_int(y_copy)

                    temp156 = temp153
                    if temp156:

                        temp158 = project_int(y_copy)
                        temp159 = project_bool(temp127)
                        temp157 = temp158 + temp159
                        temp131 = inject_int(temp157)
                    else:
                        temp161 = is_big(y_copy)
                        if temp161:
                            temp160 = is_big(temp127)
                        else:
                            temp160 = is_big(y_copy)

                        temp163 = temp160
                        if temp163:

                            temp164 = project_big(y_copy)
                            temp165 = project_big(temp127)
                            temp166 = add(temp164, temp165)
                            temp131 = inject_big(temp166)
                        else:
                            error_pyobj("Type Checking Error")

        y_copy = temp131
        temp199 = inject_int(4)
        temp170 = is_int(y_copy)
        if temp170:
            temp169 = is_int(temp199)
        else:
            temp169 = is_int(y_copy)

        temp172 = temp169
        if temp172:

            temp173 = project_int(y_copy)
            temp174 = project_int(temp199)
            temp173 = temp173 == temp174
            temp168 = inject_bool(temp173)
        else:
            temp176 = is_bool(y_copy)
            if temp176:
                temp175 = is_bool(temp199)
            else:
                temp175 = is_bool(y_copy)

            temp178 = temp175
            if temp178:

                temp179 = project_bool(y_copy)
                temp180 = project_bool(temp199)
                temp179 = temp179 == temp180
                temp168 = inject_bool(temp179)
            else:
                temp182 = is_int(y_copy)
                if temp182:
                    temp181 = is_bool(temp199)
                else:
                    temp181 = is_int(y_copy)

                temp184 = temp181
                if temp184:

                    temp185 = project_int(y_copy)
                    temp186 = project_bool(temp199)
                    temp185 = temp185 == temp186
                    temp168 = inject_bool(temp185)
                else:
                    temp188 = is_bool(y_copy)
                    if temp188:
                        temp187 = is_int(temp199)
                    else:
                        temp187 = is_bool(y_copy)

                    temp190 = temp187
                    if temp190:

                        temp191 = project_bool(y_copy)
                        temp192 = project_int(temp199)
                        temp191 = temp191 == temp192
                        temp168 = inject_bool(temp191)
                    else:
                        temp194 = is_big(y_copy)
                        if temp194:
                            temp193 = is_big(temp199)
                        else:
                            temp193 = is_big(y_copy)

                        temp196 = temp193
                        if temp196:

                            temp197 = project_big(y_copy)
                            temp198 = project_big(temp199)
                            temp197 = equal(temp197, temp198)
                            temp168 = inject_bool(temp197)
                        else:
                            error_pyobj("Type Checking Error")

        temp167 = temp168
        temp201 = is_int(temp167)
        if temp201:
            temp167 = project_int(temp167)
        else:
            temp202 = is_bool(temp167)
            if temp202:
                temp167 = project_bool(temp167)
            else:
                temp203 = is_big(temp167)
                if temp203:
                    temp167 = project_big(temp167)
                else:
                    error_pyobj("Type Checking Error")
        temp200 = inject_int(temp167)
        temp584 = is_true(temp200)
        if temp584:
            temp240 = inject_int(1)
            temp206 = is_int(z)
            if temp206:
                temp205 = is_int(temp240)
            else:
                temp205 = is_int(z)

            temp208 = temp205
            if temp208:

                temp210 = project_int(z)
                temp211 = project_int(temp240)
                temp209 = temp210 + temp211
                temp204 = inject_int(temp209)
            else:
                temp213 = is_bool(z)
                if temp213:
                    temp212 = is_bool(temp240)
                else:
                    temp212 = is_bool(z)

                temp215 = temp212
                if temp215:

                    temp217 = project_bool(z)
                    temp218 = project_bool(temp240)
                    temp216 = temp217 + temp218
                    temp204 = inject_bool(temp216)
                else:
                    temp220 = is_bool(z)
                    if temp220:
                        temp219 = is_int(temp240)
                    else:
                        temp219 = is_bool(z)

                    temp222 = temp219
                    if temp222:

                        temp224 = project_bool(z)
                        temp225 = project_int(temp240)
                        temp223 = temp224 + temp225
                        temp204 = inject_int(temp223)
                    else:
                        temp227 = is_int(z)
                        if temp227:
                            temp226 = is_bool(temp240)
                        else:
                            temp226 = is_int(z)

                        temp229 = temp226
                        if temp229:

                            temp231 = project_int(z)
                            temp232 = project_bool(temp240)
                            temp230 = temp231 + temp232
                            temp204 = inject_int(temp230)
                        else:
                            temp234 = is_big(z)
                            if temp234:
                                temp233 = is_big(temp240)
                            else:
                                temp233 = is_big(z)

                            temp236 = temp233
                            if temp236:

                                temp237 = project_big(z)
                                temp238 = project_big(temp240)
                                temp239 = add(temp237, temp238)
                                temp204 = inject_big(temp239)
                            else:
                                error_pyobj("Type Checking Error")

            z = temp204
            temp273 = inject_int(3)
            temp244 = is_int(x)
            if temp244:
                temp243 = is_int(temp273)
            else:
                temp243 = is_int(x)

            temp246 = temp243
            if temp246:

                temp247 = project_int(x)
                temp248 = project_int(temp273)
                temp247 = temp247 == temp248
                temp242 = inject_bool(temp247)
            else:
                temp250 = is_bool(x)
                if temp250:
                    temp249 = is_bool(temp273)
                else:
                    temp249 = is_bool(x)

                temp252 = temp249
                if temp252:

                    temp253 = project_bool(x)
                    temp254 = project_bool(temp273)
                    temp253 = temp253 == temp254
                    temp242 = inject_bool(temp253)
                else:
                    temp256 = is_int(x)
                    if temp256:
                        temp255 = is_bool(temp273)
                    else:
                        temp255 = is_int(x)

                    temp258 = temp255
                    if temp258:

                        temp259 = project_int(x)
                        temp260 = project_bool(temp273)
                        temp259 = temp259 == temp260
                        temp242 = inject_bool(temp259)
                    else:
                        temp262 = is_bool(x)
                        if temp262:
                            temp261 = is_int(temp273)
                        else:
                            temp261 = is_bool(x)

                        temp264 = temp261
                        if temp264:

                            temp265 = project_bool(x)
                            temp266 = project_int(temp273)
                            temp265 = temp265 == temp266
                            temp242 = inject_bool(temp265)
                        else:
                            temp268 = is_big(x)
                            if temp268:
                                temp267 = is_big(temp273)
                            else:
                                temp267 = is_big(x)

                            temp270 = temp267
                            if temp270:

                                temp271 = project_big(x)
                                temp272 = project_big(temp273)
                                temp271 = equal(temp271, temp272)
                                temp242 = inject_bool(temp271)
                            else:
                                error_pyobj("Type Checking Error")

            temp241 = temp242
            temp275 = is_int(temp241)
            if temp275:
                temp241 = project_int(temp241)
            else:
                temp276 = is_bool(temp241)
                if temp276:
                    temp241 = project_bool(temp241)
                else:
                    temp277 = is_big(temp241)
                    if temp277:
                        temp241 = project_big(temp241)
                    else:
                        error_pyobj("Type Checking Error")
            temp274 = inject_int(temp241)
            temp583 = is_true(temp274)
            if temp583:
                temp314 = inject_int(1)
                temp280 = is_int(z)
                if temp280:
                    temp279 = is_int(temp314)
                else:
                    temp279 = is_int(z)

                temp282 = temp279
                if temp282:

                    temp284 = project_int(z)
                    temp285 = project_int(temp314)
                    temp283 = temp284 + temp285
                    temp278 = inject_int(temp283)
                else:
                    temp287 = is_bool(z)
                    if temp287:
                        temp286 = is_bool(temp314)
                    else:
                        temp286 = is_bool(z)

                    temp289 = temp286
                    if temp289:

                        temp291 = project_bool(z)
                        temp292 = project_bool(temp314)
                        temp290 = temp291 + temp292
                        temp278 = inject_bool(temp290)
                    else:
                        temp294 = is_bool(z)
                        if temp294:
                            temp293 = is_int(temp314)
                        else:
                            temp293 = is_bool(z)

                        temp296 = temp293
                        if temp296:

                            temp298 = project_bool(z)
                            temp299 = project_int(temp314)
                            temp297 = temp298 + temp299
                            temp278 = inject_int(temp297)
                        else:
                            temp301 = is_int(z)
                            if temp301:
                                temp300 = is_bool(temp314)
                            else:
                                temp300 = is_int(z)

                            temp303 = temp300
                            if temp303:

                                temp305 = project_int(z)
                                temp306 = project_bool(temp314)
                                temp304 = temp305 + temp306
                                temp278 = inject_int(temp304)
                            else:
                                temp308 = is_big(z)
                                if temp308:
                                    temp307 = is_big(temp314)
                                else:
                                    temp307 = is_big(z)

                                temp310 = temp307
                                if temp310:

                                    temp311 = project_big(z)
                                    temp312 = project_big(temp314)
                                    temp313 = add(temp311, temp312)
                                    temp278 = inject_big(temp313)
                                else:
                                    error_pyobj("Type Checking Error")

                z = temp278
                temp316 = inject_int(1)
                temp317 = is_int(temp316)
                if temp317:
                    temp316 = project_int(temp316)
                    temp316 = -temp316
                    temp316 = inject_int(temp316)
                else:
                    temp318 = is_bool(temp316)
                    if temp318:
                        temp316 = project_bool(temp316)
                        temp316 = -temp316
                        temp316 = inject_bool(temp316)
                    else:
                        temp319 = is_big(temp316)
                        if temp319:
                            temp316 = project_big(temp316)
                            temp316 = -temp316
                            temp316 = inject_big(temp316)
                        else:
                            error_pyobj("Type Checking Error")
                temp322 = is_int(y)
                if temp322:
                    temp321 = is_int(temp316)
                else:
                    temp321 = is_int(y)

                temp324 = temp321
                if temp324:

                    temp326 = project_int(y)
                    temp327 = project_int(temp316)
                    temp325 = temp326 + temp327
                    temp320 = inject_int(temp325)
                else:
                    temp329 = is_bool(y)
                    if temp329:
                        temp328 = is_bool(temp316)
                    else:
                        temp328 = is_bool(y)

                    temp331 = temp328
                    if temp331:

                        temp333 = project_bool(y)
                        temp334 = project_bool(temp316)
                        temp332 = temp333 + temp334
                        temp320 = inject_bool(temp332)
                    else:
                        temp336 = is_bool(y)
                        if temp336:
                            temp335 = is_int(temp316)
                        else:
                            temp335 = is_bool(y)

                        temp338 = temp335
                        if temp338:

                            temp340 = project_bool(y)
                            temp341 = project_int(temp316)
                            temp339 = temp340 + temp341
                            temp320 = inject_int(temp339)
                        else:
                            temp343 = is_int(y)
                            if temp343:
                                temp342 = is_bool(temp316)
                            else:
                                temp342 = is_int(y)

                            temp345 = temp342
                            if temp345:

                                temp347 = project_int(y)
                                temp348 = project_bool(temp316)
                                temp346 = temp347 + temp348
                                temp320 = inject_int(temp346)
                            else:
                                temp350 = is_big(y)
                                if temp350:
                                    temp349 = is_big(temp316)
                                else:
                                    temp349 = is_big(y)

                                temp352 = temp349
                                if temp352:

                                    temp353 = project_big(y)
                                    temp354 = project_big(temp316)
                                    temp355 = add(temp353, temp354)
                                    temp320 = inject_big(temp355)
                                else:
                                    error_pyobj("Type Checking Error")

                y = temp320
                temp392 = inject_int(1)
                temp358 = is_int(x)
                if temp358:
                    temp357 = is_int(temp392)
                else:
                    temp357 = is_int(x)

                temp360 = temp357
                if temp360:

                    temp362 = project_int(x)
                    temp363 = project_int(temp392)
                    temp361 = temp362 + temp363
                    temp356 = inject_int(temp361)
                else:
                    temp365 = is_bool(x)
                    if temp365:
                        temp364 = is_bool(temp392)
                    else:
                        temp364 = is_bool(x)

                    temp367 = temp364
                    if temp367:

                        temp369 = project_bool(x)
                        temp370 = project_bool(temp392)
                        temp368 = temp369 + temp370
                        temp356 = inject_bool(temp368)
                    else:
                        temp372 = is_bool(x)
                        if temp372:
                            temp371 = is_int(temp392)
                        else:
                            temp371 = is_bool(x)

                        temp374 = temp371
                        if temp374:

                            temp376 = project_bool(x)
                            temp377 = project_int(temp392)
                            temp375 = temp376 + temp377
                            temp356 = inject_int(temp375)
                        else:
                            temp379 = is_int(x)
                            if temp379:
                                temp378 = is_bool(temp392)
                            else:
                                temp378 = is_int(x)

                            temp381 = temp378
                            if temp381:

                                temp383 = project_int(x)
                                temp384 = project_bool(temp392)
                                temp382 = temp383 + temp384
                                temp356 = inject_int(temp382)
                            else:
                                temp386 = is_big(x)
                                if temp386:
                                    temp385 = is_big(temp392)
                                else:
                                    temp385 = is_big(x)

                                temp388 = temp385
                                if temp388:

                                    temp389 = project_big(x)
                                    temp390 = project_big(temp392)
                                    temp391 = add(temp389, temp390)
                                    temp356 = inject_big(temp391)
                                else:
                                    error_pyobj("Type Checking Error")

                x = temp356
                inner_loop_done = inject_int(1)
            else:
                temp425 = inject_int(2)
                temp396 = is_int(x)
                if temp396:
                    temp395 = is_int(temp425)
                else:
                    temp395 = is_int(x)

                temp398 = temp395
                if temp398:

                    temp399 = project_int(x)
                    temp400 = project_int(temp425)
                    temp399 = temp399 == temp400
                    temp394 = inject_bool(temp399)
                else:
                    temp402 = is_bool(x)
                    if temp402:
                        temp401 = is_bool(temp425)
                    else:
                        temp401 = is_bool(x)

                    temp404 = temp401
                    if temp404:

                        temp405 = project_bool(x)
                        temp406 = project_bool(temp425)
                        temp405 = temp405 == temp406
                        temp394 = inject_bool(temp405)
                    else:
                        temp408 = is_int(x)
                        if temp408:
                            temp407 = is_bool(temp425)
                        else:
                            temp407 = is_int(x)

                        temp410 = temp407
                        if temp410:

                            temp411 = project_int(x)
                            temp412 = project_bool(temp425)
                            temp411 = temp411 == temp412
                            temp394 = inject_bool(temp411)
                        else:
                            temp414 = is_bool(x)
                            if temp414:
                                temp413 = is_int(temp425)
                            else:
                                temp413 = is_bool(x)

                            temp416 = temp413
                            if temp416:

                                temp417 = project_bool(x)
                                temp418 = project_int(temp425)
                                temp417 = temp417 == temp418
                                temp394 = inject_bool(temp417)
                            else:
                                temp420 = is_big(x)
                                if temp420:
                                    temp419 = is_big(temp425)
                                else:
                                    temp419 = is_big(x)

                                temp422 = temp419
                                if temp422:

                                    temp423 = project_big(x)
                                    temp424 = project_big(temp425)
                                    temp423 = equal(temp423, temp424)
                                    temp394 = inject_bool(temp423)
                                else:
                                    error_pyobj("Type Checking Error")

                temp393 = temp394
                temp427 = is_int(temp393)
                if temp427:
                    temp393 = project_int(temp393)
                else:
                    temp428 = is_bool(temp393)
                    if temp428:
                        temp393 = project_bool(temp393)
                    else:
                        temp429 = is_big(temp393)
                        if temp429:
                            temp393 = project_big(temp393)
                        else:
                            error_pyobj("Type Checking Error")
                temp426 = inject_int(temp393)
                temp504 = is_true(temp426)
                if temp504:
                    temp466 = inject_int(2)
                    temp432 = is_int(z)
                    if temp432:
                        temp431 = is_int(temp466)
                    else:
                        temp431 = is_int(z)

                    temp434 = temp431
                    if temp434:

                        temp436 = project_int(z)
                        temp437 = project_int(temp466)
                        temp435 = temp436 + temp437
                        temp430 = inject_int(temp435)
                    else:
                        temp439 = is_bool(z)
                        if temp439:
                            temp438 = is_bool(temp466)
                        else:
                            temp438 = is_bool(z)

                        temp441 = temp438
                        if temp441:

                            temp443 = project_bool(z)
                            temp444 = project_bool(temp466)
                            temp442 = temp443 + temp444
                            temp430 = inject_bool(temp442)
                        else:
                            temp446 = is_bool(z)
                            if temp446:
                                temp445 = is_int(temp466)
                            else:
                                temp445 = is_bool(z)

                            temp448 = temp445
                            if temp448:

                                temp450 = project_bool(z)
                                temp451 = project_int(temp466)
                                temp449 = temp450 + temp451
                                temp430 = inject_int(temp449)
                            else:
                                temp453 = is_int(z)
                                if temp453:
                                    temp452 = is_bool(temp466)
                                else:
                                    temp452 = is_int(z)

                                temp455 = temp452
                                if temp455:

                                    temp457 = project_int(z)
                                    temp458 = project_bool(temp466)
                                    temp456 = temp457 + temp458
                                    temp430 = inject_int(temp456)
                                else:
                                    temp460 = is_big(z)
                                    if temp460:
                                        temp459 = is_big(temp466)
                                    else:
                                        temp459 = is_big(z)

                                    temp462 = temp459
                                    if temp462:

                                        temp463 = project_big(z)
                                        temp464 = project_big(temp466)
                                        temp465 = add(temp463, temp464)
                                        temp430 = inject_big(temp465)
                                    else:
                                        error_pyobj("Type Checking Error")

                    z = temp430
                else:
                    temp503 = inject_int(3)
                    temp469 = is_int(z)
                    if temp469:
                        temp468 = is_int(temp503)
                    else:
                        temp468 = is_int(z)

                    temp471 = temp468
                    if temp471:

                        temp473 = project_int(z)
                        temp474 = project_int(temp503)
                        temp472 = temp473 + temp474
                        temp467 = inject_int(temp472)
                    else:
                        temp476 = is_bool(z)
                        if temp476:
                            temp475 = is_bool(temp503)
                        else:
                            temp475 = is_bool(z)

                        temp478 = temp475
                        if temp478:

                            temp480 = project_bool(z)
                            temp481 = project_bool(temp503)
                            temp479 = temp480 + temp481
                            temp467 = inject_bool(temp479)
                        else:
                            temp483 = is_bool(z)
                            if temp483:
                                temp482 = is_int(temp503)
                            else:
                                temp482 = is_bool(z)

                            temp485 = temp482
                            if temp485:

                                temp487 = project_bool(z)
                                temp488 = project_int(temp503)
                                temp486 = temp487 + temp488
                                temp467 = inject_int(temp486)
                            else:
                                temp490 = is_int(z)
                                if temp490:
                                    temp489 = is_bool(temp503)
                                else:
                                    temp489 = is_int(z)

                                temp492 = temp489
                                if temp492:

                                    temp494 = project_int(z)
                                    temp495 = project_bool(temp503)
                                    temp493 = temp494 + temp495
                                    temp467 = inject_int(temp493)
                                else:
                                    temp497 = is_big(z)
                                    if temp497:
                                        temp496 = is_big(temp503)
                                    else:
                                        temp496 = is_big(z)

                                    temp499 = temp496
                                    if temp499:

                                        temp500 = project_big(z)
                                        temp501 = project_big(temp503)
                                        temp502 = add(temp500, temp501)
                                        temp467 = inject_big(temp502)
                                    else:
                                        error_pyobj("Type Checking Error")

                    z = temp467
                temp506 = inject_int(1)
                temp507 = is_int(temp506)
                if temp507:
                    temp506 = project_int(temp506)
                    temp506 = -temp506
                    temp506 = inject_int(temp506)
                else:
                    temp508 = is_bool(temp506)
                    if temp508:
                        temp506 = project_bool(temp506)
                        temp506 = -temp506
                        temp506 = inject_bool(temp506)
                    else:
                        temp509 = is_big(temp506)
                        if temp509:
                            temp506 = project_big(temp506)
                            temp506 = -temp506
                            temp506 = inject_big(temp506)
                        else:
                            error_pyobj("Type Checking Error")
                temp512 = is_int(y)
                if temp512:
                    temp511 = is_int(temp506)
                else:
                    temp511 = is_int(y)

                temp514 = temp511
                if temp514:

                    temp516 = project_int(y)
                    temp517 = project_int(temp506)
                    temp515 = temp516 + temp517
                    temp510 = inject_int(temp515)
                else:
                    temp519 = is_bool(y)
                    if temp519:
                        temp518 = is_bool(temp506)
                    else:
                        temp518 = is_bool(y)

                    temp521 = temp518
                    if temp521:

                        temp523 = project_bool(y)
                        temp524 = project_bool(temp506)
                        temp522 = temp523 + temp524
                        temp510 = inject_bool(temp522)
                    else:
                        temp526 = is_bool(y)
                        if temp526:
                            temp525 = is_int(temp506)
                        else:
                            temp525 = is_bool(y)

                        temp528 = temp525
                        if temp528:

                            temp530 = project_bool(y)
                            temp531 = project_int(temp506)
                            temp529 = temp530 + temp531
                            temp510 = inject_int(temp529)
                        else:
                            temp533 = is_int(y)
                            if temp533:
                                temp532 = is_bool(temp506)
                            else:
                                temp532 = is_int(y)

                            temp535 = temp532
                            if temp535:

                                temp537 = project_int(y)
                                temp538 = project_bool(temp506)
                                temp536 = temp537 + temp538
                                temp510 = inject_int(temp536)
                            else:
                                temp540 = is_big(y)
                                if temp540:
                                    temp539 = is_big(temp506)
                                else:
                                    temp539 = is_big(y)

                                temp542 = temp539
                                if temp542:

                                    temp543 = project_big(y)
                                    temp544 = project_big(temp506)
                                    temp545 = add(temp543, temp544)
                                    temp510 = inject_big(temp545)
                                else:
                                    error_pyobj("Type Checking Error")

                y = temp510
                temp582 = inject_int(1)
                temp548 = is_int(x)
                if temp548:
                    temp547 = is_int(temp582)
                else:
                    temp547 = is_int(x)

                temp550 = temp547
                if temp550:

                    temp552 = project_int(x)
                    temp553 = project_int(temp582)
                    temp551 = temp552 + temp553
                    temp546 = inject_int(temp551)
                else:
                    temp555 = is_bool(x)
                    if temp555:
                        temp554 = is_bool(temp582)
                    else:
                        temp554 = is_bool(x)

                    temp557 = temp554
                    if temp557:

                        temp559 = project_bool(x)
                        temp560 = project_bool(temp582)
                        temp558 = temp559 + temp560
                        temp546 = inject_bool(temp558)
                    else:
                        temp562 = is_bool(x)
                        if temp562:
                            temp561 = is_int(temp582)
                        else:
                            temp561 = is_bool(x)

                        temp564 = temp561
                        if temp564:

                            temp566 = project_bool(x)
                            temp567 = project_int(temp582)
                            temp565 = temp566 + temp567
                            temp546 = inject_int(temp565)
                        else:
                            temp569 = is_int(x)
                            if temp569:
                                temp568 = is_bool(temp582)
                            else:
                                temp568 = is_int(x)

                            temp571 = temp568
                            if temp571:

                                temp573 = project_int(x)
                                temp574 = project_bool(temp582)
                                temp572 = temp573 + temp574
                                temp546 = inject_int(temp572)
                            else:
                                temp576 = is_big(x)
                                if temp576:
                                    temp575 = is_big(temp582)
                                else:
                                    temp575 = is_big(x)

                                temp578 = temp575
                                if temp578:

                                    temp579 = project_big(x)
                                    temp580 = project_big(temp582)
                                    temp581 = add(temp579, temp580)
                                    temp546 = inject_big(temp581)
                                else:
                                    error_pyobj("Type Checking Error")

                x = temp546
                inner_loop_done = inject_int(1)
        temp110 = inject_int(0)
        temp81 = is_int(y_copy)
        if temp81:
            temp80 = is_int(temp110)
        else:
            temp80 = is_int(y_copy)

        temp83 = temp80
        if temp83:

            temp84 = project_int(y_copy)
            temp85 = project_int(temp110)
            temp84 = temp84 != temp85
            temp79 = inject_bool(temp84)
        else:
            temp87 = is_bool(y_copy)
            if temp87:
                temp86 = is_bool(temp110)
            else:
                temp86 = is_bool(y_copy)

            temp89 = temp86
            if temp89:

                temp90 = project_bool(y_copy)
                temp91 = project_bool(temp110)
                temp90 = temp90 != temp91
                temp79 = inject_bool(temp90)
            else:
                temp93 = is_int(y_copy)
                if temp93:
                    temp92 = is_bool(temp110)
                else:
                    temp92 = is_int(y_copy)

                temp95 = temp92
                if temp95:

                    temp96 = project_int(y_copy)
                    temp97 = project_bool(temp110)
                    temp96 = temp96 != temp97
                    temp79 = inject_bool(temp96)
                else:
                    temp99 = is_bool(y_copy)
                    if temp99:
                        temp98 = is_int(temp110)
                    else:
                        temp98 = is_bool(y_copy)

                    temp101 = temp98
                    if temp101:

                        temp102 = project_bool(y_copy)
                        temp103 = project_int(temp110)
                        temp102 = temp102 != temp103
                        temp79 = inject_bool(temp102)
                    else:
                        temp105 = is_big(y_copy)
                        if temp105:
                            temp104 = is_big(temp110)
                        else:
                            temp104 = is_big(y_copy)

                        temp107 = temp104
                        if temp107:

                            temp108 = project_big(y_copy)
                            temp109 = project_big(temp110)
                            temp108 = not_equal(temp108, temp109)
                            temp79 = inject_bool(temp108)
                        else:
                            error_pyobj("Type Checking Error")

        temp78 = temp79
        temp112 = is_int(temp78)
        if temp112:
            temp78 = project_int(temp78)
        else:
            temp113 = is_bool(temp78)
            if temp113:
                temp78 = project_bool(temp78)
            else:
                temp114 = is_big(temp78)
                if temp114:
                    temp78 = project_big(temp78)
                else:
                    error_pyobj("Type Checking Error")
        temp111 = inject_int(temp78)
        temp117 = inner_loop_done
        temp118 = is_true(temp117)
        if temp118:
            temp116 = inject_bool(False)
        else:
            temp116 = inject_bool(True)
        temp115 = temp116
        temp120 = is_int(temp115)
        if temp120:
            temp115 = project_int(temp115)
        else:
            temp121 = is_bool(temp115)
            if temp121:
                temp115 = project_bool(temp115)
            else:
                temp122 = is_big(temp115)
                if temp122:
                    temp115 = project_big(temp115)
                else:
                    error_pyobj("Type Checking Error")
        temp119 = inject_int(temp115)
        temp124 = temp111
        temp125 = is_true(temp124)
        if temp125:
            temp123 = temp119
        else:
            temp123 = temp111
        temp585 = is_true(temp123)
    temp588 = inner_loop_done
    temp589 = is_true(temp588)
    if temp589:
        temp587 = inject_bool(False)
    else:
        temp587 = inject_bool(True)
    temp586 = temp587
    temp591 = is_int(temp586)
    if temp591:
        temp586 = project_int(temp586)
    else:
        temp592 = is_bool(temp586)
        if temp592:
            temp586 = project_bool(temp586)
        else:
            temp593 = is_big(temp586)
            if temp593:
                temp586 = project_big(temp586)
            else:
                error_pyobj("Type Checking Error")
    temp590 = inject_int(temp586)
    temp594 = is_true(temp590)
    if temp594:
        y = y_copy
    temp32 = inject_int(0)
    temp3 = is_int(x)
    if temp3:
        temp2 = is_int(temp32)
    else:
        temp2 = is_int(x)

    temp5 = temp2
    if temp5:

        temp6 = project_int(x)
        temp7 = project_int(temp32)
        temp6 = temp6 != temp7
        temp1 = inject_bool(temp6)
    else:
        temp9 = is_bool(x)
        if temp9:
            temp8 = is_bool(temp32)
        else:
            temp8 = is_bool(x)

        temp11 = temp8
        if temp11:

            temp12 = project_bool(x)
            temp13 = project_bool(temp32)
            temp12 = temp12 != temp13
            temp1 = inject_bool(temp12)
        else:
            temp15 = is_int(x)
            if temp15:
                temp14 = is_bool(temp32)
            else:
                temp14 = is_int(x)

            temp17 = temp14
            if temp17:

                temp18 = project_int(x)
                temp19 = project_bool(temp32)
                temp18 = temp18 != temp19
                temp1 = inject_bool(temp18)
            else:
                temp21 = is_bool(x)
                if temp21:
                    temp20 = is_int(temp32)
                else:
                    temp20 = is_bool(x)

                temp23 = temp20
                if temp23:

                    temp24 = project_bool(x)
                    temp25 = project_int(temp32)
                    temp24 = temp24 != temp25
                    temp1 = inject_bool(temp24)
                else:
                    temp27 = is_big(x)
                    if temp27:
                        temp26 = is_big(temp32)
                    else:
                        temp26 = is_big(x)

                    temp29 = temp26
                    if temp29:

                        temp30 = project_big(x)
                        temp31 = project_big(temp32)
                        temp30 = not_equal(temp30, temp31)
                        temp1 = inject_bool(temp30)
                    else:
                        error_pyobj("Type Checking Error")

    temp0 = temp1
    temp34 = is_int(temp0)
    if temp34:
        temp0 = project_int(temp0)
    else:
        temp35 = is_bool(temp0)
        if temp35:
            temp0 = project_bool(temp0)
        else:
            temp36 = is_big(temp0)
            if temp36:
                temp0 = project_big(temp0)
            else:
                error_pyobj("Type Checking Error")
    temp33 = inject_int(temp0)
    temp595 = is_true(temp33)
temp596 = z
print_any(temp596)
