
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
