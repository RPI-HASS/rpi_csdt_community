-- Local/Web deployment of pCSDT apps (Last update: 2011/12/12) --
Content:
README.txt (this file)
signfolder.bat (sample jar signing script)
Core/ (jar file of the Core and its supporting jars)
media/ (jar files necessary for pCSDT OpenGL graphics engine to work)
CC2/ (sample application)
GG/ (sample application)
SB/ (sample application)

==== Instructions to application programmers ====

1) Create a specific folder for your own application program (just like CC2/ for the Cronrow application). Put the application jar and its supporting jars to that folder.

2) Copy index.html from the CC2/ folder to your own application folder. Optional changes can be made to:
* <title>pCSDT Testing</title> (Enclosed by <title> and </title> is the title of your web page.)
* width=980 height=590 (The numbers are the the width and height of the applet window on the browser.)

3) Copy app.jnlp from the CC2/ folder to your own application folder.
The most important thing is to update the following lines.
* <jnlp> (If you are deploying the application on the web, insert an attribute "codebase" and assign it to the string representing the URL where your app.jnlp will appear in the web, e.g. odebase="http://www.ccd.rpi.edu/eglash/csdt/pcsdt/CC2". If you are targeting at local deployment (i.e. put all the folders in the same directory of a local machine, and then click on index.html or app.jnlp to start the application), leave it intact.
* <resources></resources> (Update the value assigned to "href" field of <jar href="CC.jar" main="true"/> to the jar file containing your application GUI class. If your application depends on additional jar files, list each of them as an entry in the form <jar href="Support1.jar" main="false"/><jar href="Support2.jar" main="false"/>...). If you have additional image/xml to be used by the application, you may zip thme to a jar file and include it as other jar files. Then they will be available in the relative search path. If we may skip the hostname/local full path, their relative path should be referred with a "/" at front so they are referred relative to root of the respective jar. Check CC2/app2.jnlp for an example.
* <applet-desc name="pCSDT Applet" main-class="CC.CCGui" width="1000" height="600"> (Update the value assigned to "main-class" to the GUI class of your pCSDT application. Optionally, you may update the "name", "width" and "height" values to the display name, application width and application height that you wish.). You may add <param name="xxx" value="xxx" /> children under this tag to specify applet parameters. Parameters specified here will affect applets launched with the .html file and .jnlp file. Possible parameters include "SingleDemoXmlUrl" which is for specifying the URL of a single demo xml file, "DemoPropertiesUrl" which is for specifying the URL of a .properties file including information of multiple demo xml files, "TemplateBackgroundPropertiesUrl" which is for specifying the URL of a .properties file including information of template backgrounds, and "GoalImagePropertiesUrl" which is for specifyin the URL of a .properties file including information of goal images. We also have "MainSplitLoc", "LeftSplitLoc" and "RightSplitLoc" that tell the starting locations of the main, left and right splitters in the GUI.
* If there is a critical update in the Core, you may need to move to a new Core version. This can be done by updating the line.
<extension name="pCSDT-Core" href="../Core/v1.0/Core.jnlp" /> (Change the value of "href" to the one given by the Core developer.)
Optional changes can be made to:
* <information></information> (information shown to the use before the application starts)
* <resources></resources> (If your application is NOT using OpenGL graphics engine, you may remove the following entries: <extension name="java3d-latest" href="../media/java3d/webstart/release/java3d-latest.jnlp"/> <extension name="jogl" href="../media/jogl/builds/archive/jsr-231-1.x-webstart-current/jogl.jnlp"/> <extension name="gluegen-rt" href="../media/gluegen/webstart/gluegen-rt.jnlp" />)

4) In the root folder, create your own keystore
> keytool -genkey -alias <aliasname> -keystore <keystorename>
[Optional] > keytool -selfcert -alias <aliasname> -keystore <keystorename> 
Install both ant (http://ant.apache.org/) and ant-contrib (http://ant-contrib.sourceforge.net/).
Sign your application jars with the following command.
> ant -Dfolder=XXX -Dalias=<aliasname> -Dstorepass=<keystore_password> -Dkeystore=<keystorename> Sign
where XXX is the name of the application folder.
signfolder.bat demonstrates a sample usage.

5) For local deployment, make sure you keep all the Core, media and your application folders in the same directory. Clicking on your application folder's index.html or app.jnlp will trigger your application. For web deployment, upload your app folder (and optionally the other folders if there are updates in their files) to the same directory in the web. Use your browser to point to the respective index.html to start the application.

==== Instructions to Core programmers ====

1) After you have updated Core.jar, replace the old one in the Core/ folder with your new one. If you add or remove  any supporting jars, please also make corresponding changes in that folder. Remember to update the Core.jnlp entries accordingly. If you have made a critical update on the Core (such that the old pCSDT apps can't run on the new Core), please create a new version folder to do the update. Inform the application program of the location of the new Core (../Core/vx.y/Core.jnlp where x.y is the version number).

2) In the root folder, create your own keystore
> keytool -genkey -alias <aliasname> -keystore <keystorename>
[Optional] > keytool -selfcert -alias <aliasname> -keystore <keystorename> 
Install both ant (http://ant.apache.org/) and ant-contrib (http://ant-contrib.sourceforge.net/).
Sign the Core jars with the following command.
> ant -Dfolder=Core/vx.y/ -Dalias=<aliasname> -Dstorepass=<keystore_password> -Dkeystore=<keystorename> Sign

3) Upload the Core folder to the web for web deployment.