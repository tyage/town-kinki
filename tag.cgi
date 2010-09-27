#!/usr/bin/perl

require './town_ini.cgi';
require './town_lib.pl';
require './event.pl';

	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		$size = 5000;
		$remain = $ENV{'CONTENT_LENGTH'};
		if($remain > $size){&error("サイズオーバー");}
		read(STDIN, $query, $ENV{'CONTENT_LENGTH'});
	} else {
		$query = $ENV{'QUERY_STRING'};
	}

	foreach $pair (split(/&/, $query)) {
		($key, $value) = split(/=/, $pair);
		$value =~ tr/+/ /;
		$value =~ s/%([0-9a-fA-F][0-9a-fA-F])/chr(hex($1))/eg;
			$in{$key} = $value;
	}
	
    if($in{'command'} eq "make"){
	    &header(gym_style);
        $tag_value="[$in{'tag'}$in{'mes'}]";
	    print "<center><input type=\"text\" value=\"$tag_value\" size=\"100\">";
        $tag_value =~ s/</&lt;/g;
        $tag_value =~ s/>/&gt;/g;
	    $tag_value = &tag($tag_value);
        print "<hr><table border=\"1\" width=\"90%\" bordercolor=\"#000000\" bgcolor=\"#ffffff\" cellpadding=\"5\" cellspacing=\"0\"><tr><td align=\"center\"><br>実行結果：$tag_value<br><br></td></tr></table></center>";
        exit;
    }else{
	    &header(gym_style);
	
	    print <<"EOM";
	    <table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	    <tr>
	    <td bgcolor=#ffffff>説明<br>
	    ここでは、近畿地方で使われている独自タグを自動生成することができます。<br>
	    独自タグを使うことによって、挨拶やメールなどで文字の色や太さを変えたりすることができます。<br>
	    複数の独自タグをひとつの文字に使うこともできます。<br>
	    （例：あいさつで「　[color:red,赤色の文字だべ]　」と投稿すると、<br>
	    「　<font color="red">赤色の文字だべ</font>　」と表\示されます。<br>
	    そして、それを作るには、手書きでもいいですが、ここで作っても便利だと思います。<br>
	    これを作るには、文字色（赤）を選択して、テキストに「赤色のもじだべ」と入力して「作成する」を押します。<br><br>
	    また、テキストに先ほど作成した[color:red,赤色の文字だべ]を入力、文字（太字）を選択すると、太字の赤文字ができます。<br>
	    これを投稿すると「　<b><font color="red">赤色の文字だべ</font></b>　」と、表\示されます。<br>
	    <td  bgcolor=#333333 align=center width=35%><center><font color="#ffffff" size="5">
	    <b>独<br>自<br>タ<br>グ<br>生<br>成<br>所<br>
	    </b></font></center></td>
	    </tr></table>
	    <center>
        <form method="POST" accept="game.cgi">
        <input type="hidden" name="mode" value="tag_maker">
        <input type="hidden" name="command" value="make">
	    <input type=hidden name=name value="$in{'name'}">
	    <input type=hidden name=pass value="$in{'pass'}">
        <select name="tag">
        <!--<option value="sun">画像（太陽）</option>
        <option value="cloudy">画像（雲）</option>
        <option value="typhoon">画像（台風）</option>
        <option value="rain">画像（雨）</option>
        <option value="thunder">画像（雷）</option>
        <option value="snow">画像（雪だるま）</option>
        <option value="smoking">画像（煙草）</option>
        <option value="ribbon">画像（リボン）</option>
        <option value="fog">画像（霧）</option>
        <option value="gemini">画像（人の顔）</option>
        <option value="spit">画像（人）</option>
        <option value="taurus">画像（牛）</option>
        <option value="aries">画像（羊）</option>  -->
        <option value="i,">文字（斜体）</option>
        <option value="b,">文字（太字）</option>
        <option value="u,">文字（下線）</option>
        <option value="s,">文字（打消し線）</option>
        <option value="color:red,">文字色（赤）</option>
        <option value="color:blue,">文字色（青）</option>
        <option value="color:green,">文字色（緑）</option>
        <option value="color:yellow,">文字色（黄）</option>
        <option value="bg:red,">文字背景色（赤）</option>
        <option value="bg:blue,">文字背景色（青）</option>
        <option value="bg:green,">文字背景色（緑）</option>
        <option value="bg:yellow,">文字背景色（黄）</option>
        </select>
        <input type="text" name="mes" size="100">
        <input type="submit" value="作成する">
        </form>
        </center>
EOM
        exit;
     }
exit;