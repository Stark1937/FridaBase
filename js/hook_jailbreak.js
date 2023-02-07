/*
 *  ┌─────────────────────────────────────────────────────────────┐
 *  │┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐│
 *  ││Esc│!1 │@2 │#3 │$4 │%5 │^6 │&7 │*8 │(9 │)0 │_- │+= │|\ │`~ ││
 *  │├───┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴───┤│
 *  ││ Tab │ Q │ W │ E │ R │ T │ Y │ U │ I │ O │ P │{[ │}] │ BS  ││
 *  │├─────┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴─────┤│
 *  ││ Ctrl │ A │ S │ D │ F │ G │ H │ J │ K │ L │: ;│" '│ Enter  ││
 *  │├──────┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴────┬───┤│
 *  ││ Shift  │ Z │ X │ C │ V │ B │ N │ M │< ,│> .│? /│Shift │Fn ││
 *  │└─────┬──┴┬──┴──┬┴───┴───┴───┴───┴───┴──┬┴───┴┬──┴┬─────┴───┘│
 *  │      │Fn │ Alt │         Space         │ Alt │Win│   HHKB   │
 *  │      └───┴─────┴───────────────────────┴─────┴───┘          │
 *  └─────────────────────────────────────────────────────────────┘
 * 
 * @Date         : 2017-02-21 12:46:08
 * @LastEditors  : Stark1937
 * @LastEditTime : 2023-02-07 20:01:48
 * @FilePath     : /frida/js/hook_jailbreak.js
 */


// +[DTTJailbreakDetection isJailbroken]
var mname2 = "DTTJailbreakDetection isJailbroken"
var method_m = ObjC.classes['DTTJailbreakDetection']['+ isJailbroken'];//hook 方法

if (method_m == null)
{
  console.log('Error ! Can not Find Method Addr');
}else{
	console.log('Success ! find ',mname2);
}



Interceptor.attach(method_m.implementation, {
	onEnter:function (args){
    console.log(mname2, ' in');

		console.log('\tBacktrace:\n\t' + Thread.backtrace(this.context,
		Backtracer.ACCURATE).map(DebugSymbol.fromAddress)
		.join('\n\t'));  //输出回溯

		// var arg2= ObjC.Object(args[2]);//打印第一个参数
		// console.log(arg2);

	},


	onLeave:function(retVal){
		console.log(mname2, ' onLeave...',retVal);
		retVal.replace(0x0);
	},
});
