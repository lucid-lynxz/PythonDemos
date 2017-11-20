从腾讯应用宝上下载的 `天天P图(V5.2.0.5739)` 只有1byte,所以我从百度手机市场下了一个(`V5.2.0.1706`), 版本有点区别,不过不影响;
`百度输入法` 没下载成功,我也是从百度市场上下了一个,版本一样

使用脚本 `qq_market_download.py` 来从腾讯应用宝市场下载前100的应用apk,并在当前目录下生成 `qq_market.xlsx` 文件,记录apk的一些信息;
使用脚本 `analysis_apk.py` 来对下载完成后的apk进行分析,提取其中的 `minSdkVersion` 和 `targetSdkVersion` 信息,并更新进 `qq_market.xlsx` 文件中;

需要最的是:
1. 下载apk保存时,文件名中的空格,竖线(|)以及小括号都要进行替换, 以便后续在shell中执行命令时,不会被当做特殊字符而导致命令失败;
2. 从apk中提取 `AndroidManifest.xml` ,原本是想用 `apktool` , 但是发现他反编译的manifest文件就是缺少我需要的这个标签内容,真是奇了个怪了;
    而用 `jadx` 等工具的话,倒是可以得到正确的 `manifest` 文件,但是经常会反编译失败,最后直接用的 AndroidSdk 中 aapt 工具提取,一切正常,速度也很快;
3. 通过 `aapt` 提取指定属性时,需要注意处理多个相同属性的问题, 有可能xml中存在多条 `<uses-sdk android:minSdkVersion="14" android:targetSdkVersion="23" />`;

结果:
很意外的数据, `14` 竟然占据了半壁江山, 呵呵哒, 谁能告诉我为什么? 

![minSdk分布图](https://github.com/lucid-lynxz/PythonDemos/blob/master/res/minSdkVersion%E5%88%86%E5%B8%83%E5%9B%BE.png?raw=tru)