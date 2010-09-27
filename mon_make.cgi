#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。
#################################
#　 Edit:BBQ2007/11/11
#################################
# unit.pl
#"モ投稿" => "<form method=POST action=\"mon_make.cgi\"><input type=hidden name=mode value=\"mon_make\"><input type=hidden name=name value=\"$name\"><input type=hidden name=pass value=\"$pass\"><input type=hidden name=k_id value=\"$k_id\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><td height=32 width=32><input type=image src='$img_dir/house1.gif'  onMouseOver='onMes5(\"モンスター投稿\")' onMouseOut='onMes5(\"\")'></td></form>",
#################################	
#落とすアイテム一覧
@bb_item = ("薬草","上薬草","特薬草","秘伝薬草");
#モンスター生産ログファイル
$mon_logfile="./log_dir/mon_make_log.cgi";

$this_script = "mon_make.cgi";
require './town_ini.cgi';
require './town_lib.pl';
&decode;
#メンテチェック
	if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}
$seigenyou_now_time = time;
#制限時間チェック
		$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
		if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。")}
		
#条件分岐
	if($in{'mode'} eq "mon_make"){&mon_make;}
	elsif($in{'mode'} eq "kakikomi"){&kakikomi;}
	else{&error("「戻る」ボタンで街に戻ってください");}
exit;
#######モンスター投稿表示
sub mon_make {
    foreach(@bb_item){
        $item_itiran .= "<option value=\"$_\">$_</option>";
    }
    
	&header(ginkou_style);

	print <<"EOM";
<center>
<table width="75%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi style="BACKGROUND-COLOR: #ffffff">
<tr>
<td bgcolor=#ffffff>モンスター投稿です。モンスターの投稿ができます。<br>画像は、記入しなくても\構\いません。<br>ID、落とすアイテム名、落とすアイテム番号は管理人以外はそのままで\構\いません。</td>
<td  bgcolor=#333333 align=center><Font Size="5" Color="white">モンスター投稿</Font></td>
</tr></table><br>
<form method="POST" action="$this_script">
<input type=hidden name=mode value="kakikomi">
<table cellspacing="2" cellpadding="5" width="75%" bgcolor="#ffffff" border="1">
<tr>
<td width="20%" bgcolor="#000000"><div align="center"><font color="#ffffff"><strong>ランク（s、a～d）</strong></font></div></td>
<td><input type=text name=bb_rank value="" size=10></td>
<td valign="middle" align="center" width="20%" bgcolor="#000000"><strong><font color="#ffffff">モンスター画像</font></strong></td>
<td><input type=text name=bb_gazou value=".png" size=10></td>
</tr>
<tr>
<td valign="middle" align="center" width="20%" bgcolor="#000000"><strong><font color="#ffffff">ID</font></strong></td>
<td><input type=text name=bb_id value="0" size=10></td>
<td valign="middle" align="center" width="20%" bgcolor="#000000"><strong><font color="#ffffff">落とすお金</font></strong></td>
<td><input type=text name=bb_money value="0" size=10></td>
</tr>
<tr>
<td valign="middle" align="center" width="20%" bgcolor="#000000"><strong><font color="#ffffff">モンスター名</font></strong></td>
<td><input type=text name=bb_name value="" size=10></td>
</tr>
</table>
<br>
<table cellspacing="2" cellpadding="5" width="75%" bgcolor="#ffffff" border="1">
<tr>
<td valign="middle" align="center" width="20%" bgcolor="#000000"><strong><font color="#ffffff">落とすアイテム名１</font></strong>　</td>
<td><select name="bb_itemname">
<option value="">なし</option>
$item_itiran
</select></td>
<td valign="middle" align="center" width="20%" bgcolor="#000000"><font color="#ffffff"><strong>落とすアイテム名２</strong></font></td>
<td><select name="bb_itemname2">
<option value="">なし</option>
$item_itiran
</select></td>
</tr>
<tr>
<td valign="middle" align="center" width="20%" bgcolor="#000000"><strong><font color="#ffffff">脳エネルギー</font></strong></td>
<td><input type=text name=bb_nou_energy value="0" size=10></td>
<td valign="middle" align="center" width="20%" bgcolor="#000000"><strong><font color="#ffffff">エネルギー</font></strong></td>
<td><input type=text name=bb_energy value="0" size=10></td>
</tr>
</table>
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}"><br>
<input type=submit name=kakikomi value=書き込み>
</form>
<table width="75%" border="1" cellspacing="0" cellpadding="10" align=center class=yosumi style="BACKGROUND-COLOR: #ffffff">
<tr bgcolor="#000000"><td><font color="#ffffff"><b>投稿者名</b></font></td><td><font color="#ffffff"><b>ランク</b></font></td><td><font color="#ffffff"><b>名前</b></font></td><td><font color="#ffffff"><b>画像</b></font></td><td><font color="#ffffff"><b>落とすお金</b></font></td><td><font color="#ffffff"><b>落とすアイテム</b></font></td><td><font color="#ffffff"><b>落とすアイテム２</b></font></td><td><font color="#ffffff"><b>脳エネルギー</b></font></td><td><font color="#ffffff"><b>身体エネルギー</b></font></td></tr>

EOM

	open(OL,"< $mon_logfile") || &error("Open Error : $mon_logfile");
	eval{ flock (OL, 1); };
	@mon_all = <OL>;
	close(OL);

    foreach(@mon_all){
        ($bb_rank,$bb_id,$bb_name,$bb_gazou,$bb_money,$bb_itemno,$bb_itemno2,$bb_itemname,$bb_itemname2,$bb_nou_energy,$bb_energy,$toukousya)=split(/<>/);
        
    print "<tr><td>$toukousya</td><td>$bb_rank</td><td>$bb_name</td><td>$bb_gazou</td><td>$bb_money</td><td>$bb_itemname</td><td>$bb_itemname2</td><td>$bb_nou_energy</td><td>$bb_energy</td></tr>";
    }
    print "</table><br></center><div align=\"right\"><b>Edit: neon　モンスター投稿所ver.0.82β</b><div>";
    
	&hooter("login_view","戻る");
	
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
	
	exit;
}

####書き込み処理
sub kakikomi {
	&header(syokudou_style);
    
	$aitemu_suu=@bb_item;
	$item_flag1="";
	$item_flag2="";
	$i=0;
	if($in{'bb_itemname'}){
        foreach(@bb_item) {
	        if($in{'bb_itemname'} eq $_){
	            $item_flag1="ok";
	            $item_no=$i;
	            last;
	        }
	        $i++;
        }
    }else{
	   $item_flag1="ok";
    }
    
    $i=0;
	if($in{'bb_itemname2'}){
        foreach(@bb_item) {
	        if($in{'bb_itemname2'} eq $_){
	            $item=$_;
	            $item_flag2="ok";
	            $item_no2=$i;
	            last;
	        }
	        $i++;
        }
    }else{
	   $item_flag2="ok";
    }

	if($in{'bb_itembangou'} =~ /[^0-9]/){&error("数字以外入れられません。（半角のみ）");}
	if($in{'bb_itembangou2'} =~ /[^0-9]/){&error("数字以外入れられません。（半角のみ）");}
	if($in{'bb_money'} =~ /[^0-9]/){&error("数字以外入れられません。（半角のみ）");}
	if($in{'bb_nou_energy'} =~ /[^0-9]/){&error("数字以外入れられません。（半角のみ）");}
	if($in{'bb_energy'} =~ /[^0-9]/){&error("数字以外入れられません。（半角のみ）");}
	if($in{'bb_id'} =~ /[^0-9]/){&error("数字以外入れられません。（半角のみ）");}
	if($in{'bb_name'} eq "") {&error("名前が入力されてません。");}
	if($in{'bb_money'} eq "") {&error("お金が入力されてません。");}
	if($in{'bb_nou_energy'} eq "") {&error("脳エネルギーが入力されてません。");}
	if($in{'bb_energy'} eq "") {&error("エネルギーが入力されてません。");}
	if($item_flag1 eq "" or $item_flag2 eq ""){&error("そんなアイテムありまへん。");}
	if($in{'bb_id'} eq "") {&error("IDが入力されてません。");}

	open(OL,"< $mon_logfile") || &error("Open Error : $mon_logfile");
	eval{ flock (OL, 1); };
	@mon_all = <OL>;
	close(OL);

    $mon_t="$in{'bb_rank'}<>$in{'bb_id'}<>$in{'bb_name'}<>$in{'bb_gazou'}<>$in{'bb_money'}<>$item_no<>$item_no2<>$in{'bb_itemname'}<>$in{'bb_itemname2'}<>$in{'bb_nou_energy'}<>$in{'bb_energy'}<>$in{'name'}<>\n";
	unshift (@mon_all,$mon_t);

	open(OLOUT,">$mon_logfile") || &error("$mon_logfileに書き込みが出来ません");
	eval{ flock (OL, 2); };
	print OLOUT @mon_all;
	close(OLOUT);
	&unlock;

	print <<"EOM";
<table border="1" cellspacing="1" cellpadding="5" align="center" class="yosumi">
<TR><TD>
書き込み完了<br>
</TD></TR><TR><TD>
<br><a href=\"javascript:history.back()\"> [前の画面に戻る] </a>
</TD></TR>
</table>
EOM
	&hooter("login_view","戻る");
	
	exit;
}

