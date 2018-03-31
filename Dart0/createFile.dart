import 'dart:io';
import 'dart:async';
import 'dart:convert';

void main(){
	
	print('Introduceti numele filei cu terminatia .dart');
	var line = stdin.readLineSync();
	var string = '''
/*\n FILE CREATED: ${new DateTime.now()}\n
 NAME OF FILE: ${line}\n
 AUTHOR: MIHAI CORNEL mhcrnl@gmail.com */\n
import \'dart:io\';\n
class Car { \n
	// field \n
	String name = \'Clio\'; \n
	// function \n
	void disp() { \n
		print(name); \n 
	} \n 
}\n
void main() { \n
	Car c = new Car();\n
	c.disp(); \n
}
''';

	new File(line).writeAsString(string).then((File file){

	});
}
