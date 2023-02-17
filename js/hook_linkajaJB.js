var baseAddress = Module.findBaseAddress('Seblak');
var functionAddress = baseAddress.add(0x77dc);

var fname  = 'Seblak!0x77dc';
Interceptor.attach(functionAddress, {
	onEnter:function (args){
    console.log(fname , ' in');

		// console.log('\tBacktrace:\n\t' + Thread.backtrace(this.context,
		// Backtracer.ACCURATE).map(DebugSymbol.fromAddress)
		// .join('\n\t'));  //输出回溯
	},


	onLeave:function(retVal){
		console.log(fname, ' onLeave...');
		retVal.replace(0x1);
	},
});
