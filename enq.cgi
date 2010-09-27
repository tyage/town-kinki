#!/usr/bin/perl

require './town_ini.cgi';
require './town_lib.pl';
&decode;

########################################
#スクリプト名
$this_script = 'enq.cgi';
#アンケートの選択肢最大数
$enq_max='25';
#個人アンケート選択肢＆投票数
$enq_data="member/$in{'enq_id'}/enq_data.cgi";
#個人アンケート投票者一覧
$enq_mem="member/$in{'enq_id'}/enq_member.cgi";
########################################

$in{"sentaku"} =~ s/</&lt;/g;
$in{"sentaku"} =~ s/>/&gt;/g;
$in{"title"} =~ s/</&lt;/g;
$in{"title"} =~ s/>/&gt;/g;
$in{"enq_tuika"} =~ s/</&lt;/g;
$in{"enq_tuika"} =~ s/>/&gt;/g;

#=====　メンテチェック　=====#
if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}
	
#=====　制限時間チェック　=====#
$seigenyou_now_time = time;
$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。")}

#=====　条件分岐　=====#
if($in{'mode'} eq "top"){&top;}
elsif($in{'mode'} eq "make"){&make;}
elsif($in{'mode'} eq "itiran"){&itiran;}
elsif($in{'mode'} eq "setup"){&setup;}
elsif($in{'mode'} eq "add"){&add;}
elsif($in{'mode'} eq "write"){&write;}
elsif($in{'mode'} eq "delete"){&delete;}
elsif($in{'mode'} eq "all_delete"){&all_delete;}
else{&error("「戻る」ボタンで街に戻ってください");}

exit;

#--------------------
#トップ
#--------------------
sub top{
	$comand="アンケート作成";
	$mada="on";
	$seigen="25";

	open(OUT,"$enq_all") || &error("open Error : $enq_all");
	eval{ flock (OUT, 2); };
	foreach(<OUT>){
		chomp ($_);
		($enq_id,$enq_title,$enq_name,$enq_kazu,$enq_ninzuu,$enq_seigen,$enq_special)=split(/<>/);
		if($enq_id==$k_id){
			$my_enq_title=$enq_title;
			$mada="off";
			$comand="アンケート設定";
			$seigen=$enq_seigen;
			if($enq_special eq "on"){$special=" checked";}
		}
		if($enq_name eq $admin_name){
			$itiran .= "<tr><td><input type=\"radio\" name=\"enq_id\" id=\"$enq_id\" value=\"$enq_id\"><label for=\"$enq_id\"><font color=\"red\"><b>$enq_title</b></font></label></td><td>管理人</td></tr>";
		}elsif($enq_special eq "on"){
			$itiran .= "<tr><td><input type=\"radio\" name=\"enq_id\" id=\"$enq_id\" value=\"$enq_id\"><label for=\"$enq_id\"><font color=\"red\">$enq_title</font></label></td><td>$enq_nameさん</td></tr>";
		}else{
			$itiran .= "<tr><td><input type=\"radio\" name=\"enq_id\" id=\"$enq_id\" value=\"$enq_id\"><label for=\"$enq_id\">$enq_title</td><td>$enq_nameさん</label></td></tr>";
		}
	}
	close(OUT);
	
	if($mada eq "off"){
		open(IN,"$enq_data") || &error("open Error : $enq_data");
		eval{ flock (IN, 2); };
		foreach(<IN>){
			chomp $_;
			($sentakusi,$kazu)=split(/<>/);
			$sentaku.="<option value=\"$sentakusi\">$sentakusi（$kazu票）";
		}
		close(IN);
		
		$enq_message = <<"EOM";
<form method="POST" action="$this_script">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>add<>">
<input type=hidden name=enq_id value="$k_id">
<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi>
<tr><td>
<div class=tyuu>■選択肢追加</div>
●選択肢（１つ１つ追加します。）<br>
<input type=text name="sentaku" size=120><br>
<input type=submit value="選択肢追加">
</td></tr></table>
</form>

<form method="POST" action="$this_script">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>delete<>">
<input type=hidden name=enq_id value="$k_id">
<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi>
<tr><td>
<div class=tyuu>■アンケート滅却</div>
●消す選択肢<br>
<select name="delete">$sentaku</select>
<input type=button value="これを消しちゃる！" onclick="if( confirm('ほんまにこれ消しちゃうの？') ){this.form.submit();}">
</form>
<form method="POST" action="$this_script">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>all_delete<>">
<input type=hidden name=enq_id value="$k_id">
<input type=button value="ぜええんぶ消してまう！" onclick="if( confirm('ほんまにぜえんぶ消しちゃうの？') ){this.form.submit();}">
<br>（これをするとアンケートのデータを全部消すことができます。また、投票する側も再び投票することができます。）
</form>
</td></tr></table>	
EOM
	}

	&header(syokudou_style);
	print <<"EOM";
<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
<tr>
<td bgcolor=#ffffff>ここはアンケート工場です。<br>アンケートに答えることでお金やＫポイントがもらえます。<br>アンケートの大量作成は禁止です。<br>Ｋポイント５０Ｐ払ってスペシャルアンケートにすると、特典がつきます！<br>特典としては、投票者が２ＰのＫポイントがもらえる、などがあります。</td>
<td bgcolor="#333333" align="center" width="35%" valign="center"><h1><font color="#ffffff">アンケート工場</font></h1></td>
</tr></table><br>

<form method="POST" action="$this_script">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>setup<>">
<input type=hidden name=enq_id value="$k_id">
<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi>
<tr><td>
<div class=tyuu>■$comand</div>
●アンケートタイトル<br>
<input type=text name="title" size=120 value="$my_enq_title"><br>
●投票制限人数（投票人数を制限します[1～100]）　　<input type=text name="seigen" size=10 value="$seigen"><br>
●<label for="special">スペシャルアンケート（Ｋポイント５０Ｐ消費）</label>　　　<input type="checkbox" name="special" $special><br>
<input type=submit value="$comand">
</td></tr></table>
</form>

$enq_message

<form method="POST" action="$this_script">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>itiran<>">
<table width="90%" border="3" cellspacing="0" cellpadding="3" align="center" class="yosumi">
<tr><td colspan="2">
<div class=tyuu>■アンケート一覧</div>
</td></tr>
<tr><td align="center" bgcolor="#999999"><font color="#ffffff"><b>アンケートタイトル</b></font></td><td align="center" bgcolor="#999999"><font color="#ffffff"><b>作成者</b></font></td></tr>
$itiran
<tr><td colspan="2" align="center">
<input type=submit value="アンケートを見る">
</form>
</td></tr></table>
EOM
	
	&hooter("login_view","街に戻る");
	
	exit;
}

#--------------------
#アンケート表示
#--------------------
sub itiran{
	if(!$in{'enq_id'}){&error("すいませんＩＤが取れなかったようです。もう一度やり直してください。");}
	
	if($happend_touhyou){
		$happend_print = <<"EOM";
		<script type="text/JavaScript"><!-- 
			function enq_close(){
				document.getElementById("table").width = "250";
				document.getElementById("box").style.display = "none";
				document.getElementById("title").innerHTML = "<span onclick='enq_open()' style='CURSOR:pointer;color:#ffffff;'>○開く</span>";
			}
			function enq_open(){
				document.getElementById("table").width = "";
				document.getElementById("box").style.display = "block";
				document.getElementById("title").innerHTML = "<span onclick='enq_close()' style='CURSOR:pointer;color:#ffffff;'>×閉じる</span>";
			}
		  --></script>
		<table cellpadding="5" cellspacing="0" style="position:absolute;top:0;z-index:1;right:10;border: solid 3px #8080C0;" id="table">
			<tr bgcolor="#8080C0">
				<td align="left"><font color="#ffffff">投票しました。</font></td>
				<td align="right" id="title"><span onclick="enq_close()" style="CURSOR:pointer;color:#ffffff;">×閉じる</span></td>
			</tr>
			<tr id="box" bgcolor="#ffffff">
				<td colspan="2">$happend_touhyou</td>
			</tr>
		</table>
EOM
	}
	
	open(OUT,"$enq_all") || &error("open Error : $enq_all");
	eval{ flock (OUT, 2); };
	foreach(<OUT>){
		chomp ($_);
		($enq_id,$enq_title,$enq_name,$enq_kazu,$enq_ninzuu,$enq_seigen,$enq_special)=split(/<>/);
		if($in{'enq_id'}==$enq_id){last;}
	}
	close(OUT);
	
	open(OUT,"$enq_mem") || &error("open Error : $enq_mem");
	@enq_mem=<OUT>;
	foreach(@enq_mem){
		chomp ($_);
		if($_ eq $name){
			$sudeni = "<br><br><font color=\"red\"><b>（※既に投票しています。）</b></font>";
			$select_able = "disabled";
			$submit_able = "disabled";
			$text_able = "disabled";
			last;
		}
	}
	close(OUT);
	
	open(OUT,"$enq_data") || &error("open Error : $enq_data");
	@enq_data=<OUT>;
	close(OUT);
	foreach(@enq_data){
		($sentaku,$kazu)=split(/<>/);
		$all_kazu += $kazu;
	}
	foreach(@enq_data){
		($sentaku,$kazu)=split(/<>/);
		if($all_kazu){
			$enq_width = int(($kazu / $all_kazu)*250);
		}
		$printenq .= <<"EOM";
<tr>
<td><input type="radio" name="sentaku" value="$sentaku" id="$sentaku" $select_able><label for="$sentaku">$sentaku</label></td>
<td><img src="$img_dir/energy_ao.gif" width="$enq_width" height="8">（$kazu票）</td>
</tr>
EOM
	}
	
	&header(item_style);
	print <<"EOM";
$happend_print
<div align=center><br><table border=0 cellspacing="5" cellpadding="0" width=90% style="$message_win"><tr><td>
$enq_nameさんのアンケート<br>
<b>$enq_title</b>$sudeni<hr>
<form action="enq.cgi" method="POST">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>write<>">
<input type=hidden name=enq_id value="$enq_id">
<input type=hidden name=enq_name value="$enq_name">
<input type=hidden name=enq_title value="$enq_title">
<table cellpadding="3" cellspacing="0" border="1" width="95%" align="center">
	<tr bgcolor="#999999" align="center"><td width="50%"><font color="#ffffff"><b>選択肢</b></font></td><td width="50%"><font color="#ffffff"><b>投票数</b></font></td></tr>
	$printenq
	<tr><td colspan="2"><input type="radio" name="sentaku" id="sentaku" value="" $select_able><label for="sentaku">その他（選択肢追加）</label><input type="text" name="enq_tuika" size="50" $text_able></td></tr>
</table>
<br>
<center><input type="submit" value="レッツ投票！" $submit_able></center>
</form>
</td></tr></table><br>
<form method=POST action="$this_script">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>top<>">
<input type=hidden name=enq_id value="$k_id">
<input type=submit value="アンケート工場に戻る">
</form></div>
EOM
	&hooter("login_view","街に戻る");

	exit;
}

#--------------------
#アンケート作成
#--------------------
sub setup{
	if(!$in{'enq_id'}){&error("すいませんＩＤが取れなかったようです。もう一度やり直してください。");}
	if(!$in{'title'}){$in{'title'}="無題";}
	if(!$in{'seigen'}){&error("投票制限人数を決めてください。");}
	if($in{'seigen'} < 1 || $in{'seigen'} > 100){&error("投票制限人数は１～１００です。");}
	if (length($in{'title'}) > 200) {&error("100文字以内に収めてください。");}

	#全体ログ更新#
	open(AL,"+< $enq_all") || &error("open Error : $enq_all");
	eval "flock(AL, 2);";
	@all_enq_data=<AL>;
	
	foreach(@all_enq_data){	
		chomp ($_);
		($enq_id,$enq_title,$enq_name,$enq_kazu,$enq_ninzuu,$enq_seigen,$enq_special)=split(/<>/);
		if($in{'name'} eq $enq_name){	
			$message="アンケートの設定をしました。";
			$flag="1";
			$enq_title=$in{'title'};
			$enq_seigen=$in{'seigen'};
			if($enq_special ne "on" and $in{'special'} eq "on"){
				if($kpoint<50){&error("Ｋポイントが足りないよ。");}
				$kpoint-=50;
				$message .="<br>スペシャルアンケートにしたのでＫポイント５０Ｐを支払いました。";
			}
			$enq_special=$in{'special'};
		}
		push @new_enq_data,"$enq_id<>$enq_title<>$enq_name<>$enq_kazu<>$enq_ninzuu<>$enq_seigen<>$enq_special<>\n";
	}
	
	if(!$flag){
		$message="アンケートを作成しました。";
		if($in{'special'} eq "on"){
			if($kpoint<50){&error("Ｋポイントが足りないよ。");}
			$kpoint-=50;
			$message .="<br>スペシャルアンケートですので評価ポイント５０Ｐを支払いました。";
		}
		unshift @new_enq_data,"$in{'enq_id'}<>$in{'title'}<>$in{'name'}<>1<>0<>$in{'seigen'}<>$in{'special'}<>\n";
	}
	
	seek(AL, 0, 0);
	print AL @new_enq_data;
	truncate(AL, tell(AL));
	close(AL);
	
	#ログの作成#
	if (! -e $enq_data){
		open(CPB,">$enq_data") || &error("Write Error : $enq_data");
		eval{ flock (CPB, 2); };
		chmod 0666,"$enq_data";
		close(CPB);
	}
	if (! -e $enq_mem){
		open(CPB,">$enq_mem") || &error("Write Error : $enq_mem");
		eval{ flock (CPB, 2); };
		chmod 0666,"$enq_mem";
		close(CPB);
	}
	
	#メッセージ表示#
	&header(item_style);
	print <<"EOM";
<div align=center><br><table border=0 cellspacing="5" cellpadding="0" width=500 style="$message_win"><tr><td>$message</td></tr></table><br>
<form method=POST action="$this_script">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>top<>">
<input type=hidden name=enq_id value="$k_id">
<input type=submit value="アンケート工場に戻る">
</form></div>
EOM
	
	&hooter("login_view","街に戻る");
	
	#自分のログ更新#
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
	
exit;
}

#--------------------
#選択肢追加
#--------------------
sub add{
	if(!$in{'sentaku'}){&error("選択肢を作ってください");}
	if(!$in{'enq_id'}){&error("すいませんＩＤが取れなかったようです。もう一度やり直してください。");}
	if (length($in{'sentaku'}) > 100) {&error("50文字以内に収めてください。");}

	#全体ログ確認#
	open(AL,"< $enq_all") || &error("open Error : $enq_all");
	eval "flock(AL, 2);";
	@all_enq_data=<AL>;
	foreach(@all_enq_data){
		chomp ($_);
		($enq_id,$enq_title,$enq_name,$enq_kazu,$enq_ninzuu,$enq_seigen,$enq_special)=split(/<>/);
		if($in{'name'} eq $enq_name){
			$flag="1";
			$enq_kazu++;
		}
		push @new_enq_data,"$enq_id<>$enq_title<>$enq_name<>$enq_kazu<>$enq_ninzuu<>$enq_seigen<>$enq_special<>\n";
	}
	if(!$flag){&error("あれ？ないよ？");}
	close(AL);
	
	#データログ更新#
	open(IN,"< $enq_data") || &error("Write Error : $enq_data");
	eval{ flock (IN, 2); };
	@enq_data=<IN>;
	$sentaku_suu=@enq_data;
	if($sentaku_suu >= $enq_max){&error("選択肢は最大$enq_maxです");}
	push @enq_data,"$in{'sentaku'}<>0<>\n";
	close(IN);
	
	#ログ更新#
	open(OUT,"> $enq_all") || &error("Write Error : $enq_all");
	eval{ flock (OUT, 2); };
	print OUT @new_enq_data;
	close(OUT);
	
	open(OUT2,"> $enq_data") || &error("Write Error : $enq_data");
	eval{ flock (OUT2, 2); };
	print OUT2 @enq_data;
	close(OUT2T);
	
	#メッセージ表示#
	&header(item_style);
	print <<"EOM";
<div align=center><br><table border=0 cellspacing="5" cellpadding="0" width=500 style="$message_win"><tr><td>選択肢を追加しました。</td></tr></table><br>
<form method=POST action="$this_script">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>top<>">
<input type=hidden name=enq_id value="$k_id">
<input type=submit value="アンケート工場に戻る">
</form></div>
EOM
	
	&hooter("login_view","街に戻る");
	
	#自分のログ更新#
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
	
exit;
}

#--------------------
#アンケート投票
#--------------------
sub write{	
	if($in{'enq_tuika'}){$kaitou = $in{'enq_tuika'};}
	elsif($in{'sentaku'}){$kaitou = $in{'sentaku'};}
	else{&error("選択肢を選んでください。");}
	
	if (length($kaitou) > 100) {&error("50文字以内に収めてください。");}
	if(!$in{'enq_id'}){&error("すいませんＩＤが取れなかったようです。もう一度やり直してください。");}
	if($in{'enq_tuika'} and $in{'sentaku'} ne ""){&error("その他と選択肢の２つも選べまへん。欲張ったあかんがな。");}
	if($in{'enq_id'}==$k_id){&error("作成者は無理だってさ。");}
	
	#全体ログにあるかどうか#
	open(AL,"< $enq_all") || &error("Open Error : $enq_all");
	eval{ flock (AL, 2); };
	@all_enq_data = <AL>;
	foreach(@all_enq_data){
		chomp ($_);
		($enq_id,$enq_title,$enq_name,$enq_kazu,$enq_ninzuu,$enq_seigen,$enq_special)=split(/<>/);
		if($in{'enq_name'} eq $enq_name){
			if(!$enq_seigen){$enq_seigen="25";}
			if($enq_seigen<=$enq_ninzuu){&error("投票制限人数超えてるよ");}
			$flag="1";
			$special=$enq_special;
			$enq_ninzuu++;
		}
		push @new_enq_data,"$enq_id<>$enq_title<>$enq_name<>$enq_kazu<>$enq_ninzuu<>$enq_seigen<>$enq_special<>\n";
	}
	if(!$flag){&error("そんなアンケートないよ。");}
	close(AL);
	
	#メンバーログ更新#
	open(ME,"< $enq_mem") || &error("Write Error : $enq_mem");
	eval{ flock (ME, 2); };
	@enq_member=<ME>;
	foreach(@enq_member){
		chomp ($_);
		if($in{'name'} eq $_){&error("多重投票禁止です");}
		push @new_member,"$_\n";
	}
	unshift @new_member,"$in{'name'}\n";
	close(ME);
	
	#データログ更新#
	open(IN,"< $enq_data") || &error("Write Error : $enq_data");
	eval{ flock (IN, 2); };
	@enq_data=<IN>;
	foreach(@enq_data){
		chomp $_;
		($sentaku,$kazu)=split(/<>/);
		if($in{'enq_tuika'}){
			if($in{'enq_tuika'} eq $sentaku){&error("既にその選択肢はありまっせ。");}
		}elsif($sentaku eq $in{'sentaku'}){
			$kazu++;
		}
		push @new_data,"$sentaku<>$kazu<>\n";
	}
	if($in{'enq_tuika'}){
		$sentaku_suu=@new_data;
		if($sentaku_suu >= $enq_max){&error("選択肢は最大$enq_maxです");}
		push @new_data,"$in{'enq_tuika'}（$in{'name'}さん作成）<>1<>\n";
	}
	close(IN);
	
	#ログ更新
	open(OUT1,"> $enq_mem") || &error("Write Error : $enq_mem");
	eval{ flock (OUT1, 2); };
	print OUT1 @new_member;
	close(OUT1);
	
	open(OUT2,"> $enq_data") || &error("Write Error : $enq_data");
	eval{ flock (OUT2, 2); };
	print OUT2 @new_data;
	close(OUT2);
	
	open(OUT3,"> $enq_all") || &error("Write Error : $enq_all");
	eval{ flock (OUT3, 2); };
	print OUT3 @new_enq_data;
	close(OUT3);
	
	#自分のログ更新#
	$randed += int(rand(10))+1;
	if ($special ne "on" and $randed == 7){
		$randed += int(rand(10000))+5000;
		$money += $randed;
		$kpoint += 2;
		$happend_touhyou = "●ボーナスです！$randed円のお金をゲットしました。<br>　あと、Ｋポイントも２Ｐもらえました！";
	}elsif($special eq "on" and $randed == 7){
		$randed += int(rand(20000))+10000;
		$money += $randed;
		$kpoint+=3;
		$happend_touhyou = "●ボーナスです！$randed円のお金をゲットしました。<br>　あと、Ｋポイントも３Ｐもらえました！";
	}elsif($special eq "on"){
		$randed += int(rand(4000))+2000;
		$money += $randed;
		$kpoint+=2;
		$happend_touhyou = "●$randed円のお金を得ました。<br>　Ｋポイントが２Ｐもらえました！";
	}else{
		$randed += int(rand(1000))+1000;
		$money += $randed;
		$kpoint++;
		$happend_touhyou = "●$randed円のお金を得ました。<br>　Ｋポイントが１Ｐもらえました！";
	}
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
	
	#メッセージ表示#
	&itiran;
	
	exit;
}

#--------------------
#選択肢消去
#--------------------
sub delete{

	if(!$in{'delete'}){&error("選択肢を書いてください");}
	if(!$in{'enq_id'}){&error("すいませんＩＤが取れなかったようです。もう一度やり直してください。");}
	
	#データログ更新#
	open(AL,"+< $enq_data") || &error("open Error : $enq_data");
	eval "flock(AL, 2);";
	@enq_data=<AL>;
	$delete_flag='0';
	foreach(@enq_data){
	chomp $_;
	($sentaku,$kazu)=split(/<>/);
		if($sentaku eq $in{'delete'}){
			$delete_flag='1';
			next;
		}else{	
			push @new_delete,"$sentaku<>$kazu<>\n";
		}
	}
	seek(AL, 0, 0);
	print AL @new_delete;
	truncate(AL, tell(AL));
	close(AL);
	if(!$delete_flag){&error("残念だったな。そんな選択肢はないらしいよ。");}
	
	#全体ログ更新#
	open(AL,"+< $enq_all") || &error("open Error : $enq_all");
	eval "flock(AL, 2);";
	@all_enq_data=<AL>;
	foreach(@all_enq_data){
	chomp ($_);
	($enq_id,$enq_title,$enq_name,$enq_kazu,$enq_ninzuu,$enq_seigen,$enq_special)=split(/<>/);
	if($in{'name'} eq $enq_name){$enq_kazu--;}	
		push @new_enq_data,"$enq_id<>$enq_title<>$enq_name<>$enq_kazu<>$enq_ninzuu<>$enq_seigen<>$enq_special<>\n";
	}
	seek(AL, 0, 0);
	print AL @new_enq_data;
	truncate(AL, tell(AL));
	close(AL);
	
	#メッセージ表示#
	&header(item_style);
	print <<"EOM";
<div align=center><br><table border=0 cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>選択肢『$in{'delete'}』を消しましたよん。</td></tr></table><br>
<form method=POST action="$this_script">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>top<>">
<input type=hidden name=enq_id value="$k_id">
<input type=submit value="アンケート工場に戻る">
</form></div>
EOM

	&hooter("login_view","街に戻る");
	
	exit;
}

#--------------------
#アンケート全消去
#--------------------
sub all_delete{
	if(!$in{'enq_id'}){&error("すいませんＩＤが取れなかったようです。もう一度やり直してください。");}
	
	#データログ更新#
	open(AL,"+> $enq_data") || &error("open Error : $enq_data");
	eval "flock(AL, 2);";
	close(AL);
	
	#データログ更新#
	open(AL,"+> $enq_mem") || &error("open Error : $enq_mem");
	eval "flock(AL, 2);";
	close(AL);
	
	#全体ログ更新#
	open(AL,"+< $enq_all") || &error("open Error : $enq_all");
	eval "flock(AL, 2);";
	foreach(<AL>){
		chomp ($_);
		($enq_id,$enq_title,$enq_name,$enq_kazu,$enq_ninzuu,$enq_seigen,$enq_special)=split(/<>/);
		if($in{'name'} eq $enq_name){next;}
		push @new_enq_data,"$enq_id<>$enq_title<>$enq_name<>$enq_kazu<>$enq_ninzuu<>$enq_seigen<>$enq_special<>\n";
	}
	seek(AL, 0, 0);
	print AL @new_enq_data;
	truncate(AL, tell(AL));
	close(AL);
	
	#メッセージ表示#
	&header(item_style);
	print <<"EOM";
<div align=center><br><table border=0 cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>アンケートを全部消しましたよん。</td></tr></table><br>
<form method=POST action="$this_script">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>top<>">
<input type=hidden name=enq_id value="$k_id">
<input type=submit value="アンケート工場に戻る">
</form></div>
EOM

	&hooter("login_view","街に戻る");
	
	exit;
}