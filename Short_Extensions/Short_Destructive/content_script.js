
function fib(){
    var a = 1;
    var b = 1;
    var c = 1;
    var d = []
    while(true){
        c = a+b
        a = b
        b = c
        d.push(c)
    }


}

//fib()