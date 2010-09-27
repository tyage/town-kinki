#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。
#################################
#　８ラインスロット(改５ライン)
#  オリジナル　「ゆかにゃん」さん
#　改造 Edit:たっちゃん　2006/12/07
#################################

################ unit.pl 追加 #################
# "スロット" => "<form method=POST action=\"slot.cgi\"><input type=hidden name=mode value=\"l1_slot\"><input type=hidden name=name value=\"$name\"><input type=hidden name=pass value=\"$pass\"><input type=hidden name=k_id value=\"$k_id\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><td height=32 width=32><input type=image src='$img_dir/donuts_tate.gif'  onMouseOver='onMes5(\"スロットで遊ぼう。\")' onMouseOut='onMes5(\"\")'></td></form>",

###############################################

$this_script = 'slot.cgi'; # パーミッション 700 755
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
	if($in{'mode'} eq "l1_slot"){&l1_slot;}
	if($in{'mode'} eq "saikoro"){&saikoro;} #koko 2005/05/15

	else{&error("「戻る」ボタンで街に戻ってください");}
exit;

sub l1_slot{

	&header(ginkou_style);

	#同じ人が続けてできるかどうか（１．できる　０.できない）
	$l1_set1 = 1;
	
	#↑で１を選んだときの時間間隔（秒）０だと好きなだけ回せます。
	$l1_set2 = 60;
	
	#5ラインスロットのログファイル
	#設定したファイルをアップして書き込み可能のパーミッションに設定をしてください。
	$l1_log = "./log_dir/l1_log.cgi"; # パーミッション 600 666
	
	#１ゲームあたりの料金（ここを増やしたり変えればいろんな料金になります）
	@l1_stt3 = ('500','1000','5000','10000','100000','1000000');
	
	#小倍率はステータス還元 ('yes','no')
	$sutetasu_on = 'yes';
	#ステータスの倍率
	@sutetasu_bai = (0,1,2,3,4,5);

	@sutetasu_name = ("国語","数学","理科","社会","英語","音楽","美術","ルックス","体力","健康","スピード","パワー","腕力","脚力","love","面白さ","Ｈ");

	#スロットの代金を所持して無くてもできるか（０．できない　１.できる）
	$l1_ste4 = 0;
	
	#当たった時、元金を引く　('yes','no')
	$motokin_hiku = 'yes';

	#各リール設定
	#リールは左から１２３になっています
	#絵柄は０から６までの７種類
	#0が一番出やすい物６が出にくいものと考えてください。
	
	#第1リール設定
	@l1_l1=('0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','1','1','1','1','2','2','2','2','2','3','3','3','3','4','4','4','5','5','6');
	
	#第2リール設定
	@l1_l2=('0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','1','1','1','1','2','2','2','2','2','3','3','3','3','4','4','4','5','5','6');
	
	#第3リール設定
	@l1_l3=('0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','1','1','1','1','2','2','2','2','2','3','3','3','3','4','4','4','5','5','6');

	#絵柄の倍率設定
	#左から０がそろったときの絵柄となっています。
	@l1_bauritu=('1','20','80','200','800','2000','7777');
	
	#スロット用の画像のフォルダー名
	#httpから始まるものでも相対パスでもおけです。最後は/にしてください
	$l1_img="./img/slot/";
	
	#設定終了
	
	#データ読み込み
	open(MA,"< $l1_log") || &error("$l1_logが開けません");
	eval{ flock (MA, 1); };
	@l1_data = <MA>;
	close(MA);
	($l1_name,$l1_time,$j_liru1,$j_liru2,$j_liru3,$atare,$in_rate,$coment2)= split(/<>/, $l1_data[0]);

	#スロットをした処理
	if($in{'command'} eq "slot_ok"){
		@liru1m = &randcheck($#l1_l1,3);
		@liru2m = &randcheck($#l1_l2,3);
		@liru3m = &randcheck($#l1_l3,3);
#koko2006/12/08
		@liru1 = ($l1_l1[$liru1m[0]],$l1_l2[$liru2m[0]],$l1_l3[$liru3m[0]]);
		@liru2 = ($l1_l1[$liru1m[1]],$l1_l2[$liru2m[1]],$l1_l3[$liru3m[1]]);
		@liru3 = ($l1_l1[$liru1m[2]],$l1_l2[$liru2m[2]],$l1_l3[$liru3m[2]]);
#kokoend
		$now_time = time ;
		#前回のゲームをした人と自分が一緒かを調べる
		if($l1_name eq $name){
			#同じ人だった場合が出来るか
			if($l1_set1 == 1){
				#出来る場合の時間間隔処理
				if($l1_time + $l1_set2 > $now_time){
					&error("$l1_set2秒お待ち下さい。","modori");
				}
			}else { #同じ人はできない）
				&error("同じ人は続けてプレーすることが出来ません。");
			}
		}
		#所持金ちぇっく
		if($in{'rate'} > $money && $l1_ste4==0){
			&error("所持金が足りません。");
		}
		if($in{'rate'} < 0){
			&error("不正入力です。");
		}
		$atari = "";
		$disp = "";
		$atarikane = 0;

		if ($sutetasu_on eq 'yes'){
			$i = 0;
			for (0 .. $#l1_stt3){
				if ($in{'rate'} == $l1_stt3[$i]){$sute_bai = $sutetasu_bai[$i];}
				$i++;
			}
		}

#test $liru1[0] =1;$liru2[1] =1;$liru3[2] =1;#test

		if($liru1[1] == $liru2[1] && $liru2[1] ==$liru3[1]){
			if ($sutetasu_on eq 'yes'){
				if ($l1_bauritu[$liru1[1]] == $l1_bauritu[0]){
					$s_rand =int(rand($#sutetasu_name + 1));
					$s_name = $sutetasu_name[$s_rand];
					&sutetasu_up("$s_name","$sute_bai");
					$coment .= "$s_name+$sute_bai<br>";
				}else{
					$atare_d = $in{'rate'} * $l1_bauritu[$liru1[1]];
					$atarikane += $atare_d;
					$disp .= "$in{'rate'}×$l1_bauritu[$liru1[1]] = $atare_d<br>";
				}
			}else{
				$atare_d = $in{'rate'} * $l1_bauritu[$liru1[1]];
				$atarikane += $atare_d;
				$disp .= "$in{'rate'}×$l1_bauritu[$liru1[1]] = $atare_d<br>";
			}
		}

		if($liru1[0] == $liru2[0] && $liru2[0] ==$liru3[0]){
			if ($sutetasu_on eq 'yes'){
				if ($l1_bauritu[$liru1[0]] == $l1_bauritu[0]){
					$s_rand =int(rand($#sutetasu_name + 1));
					$s_name = $sutetasu_name[$s_rand];
					&sutetasu_up("$s_name","$sute_bai");
					$coment .= "$s_name+$sute_bai<br>";
				}else{
					$atare_d = $in{'rate'} * $l1_bauritu[$liru1[0]];
					$atarikane += $atare_d;
					$disp .= "$in{'rate'}×$l1_bauritu[$liru1[0]] = $atare_d<br>";
				}
			}else{
				$atare_d = $in{'rate'} * $l1_bauritu[$liru1[0]];
				$atarikane += $atare_d;
				$disp .= "$in{'rate'}×$l1_bauritu[$liru1[0]] = $atare_d<br>";
			}
		}
		if($liru1[2] == $liru2[2] && $liru2[2] ==$liru3[2]){
			if ($sutetasu_on eq 'yes'){
				if ($l1_bauritu[$liru1[2]] == $l1_bauritu[0]){
					$s_rand =int(rand($#sutetasu_name + 1));
					$s_name = $sutetasu_name[$s_rand];
					&sutetasu_up("$s_name","$sute_bai");
					$coment .= "$s_name+$sute_bai<br>";
				}else{
					$atare_d = $in{'rate'} * $l1_bauritu[$liru1[2]];
					$atarikane += $atare_d;
					$disp .= "$in{'rate'}×$l1_bauritu[$liru1[2]] = $atare_d<br>";
				}
			}else{
				$atare_d = $in{'rate'} * $l1_bauritu[$liru1[2]];
				$atarikane += $atare_d;
				$disp .= "$in{'rate'}×$l1_bauritu[$liru1[2]] = $atare_d<br>";
			}
		}
		if($liru1[0] == $liru2[1] && $liru2[1] ==$liru3[2]){
			if ($sutetasu_on eq 'yes'){
				if ($l1_bauritu[$liru1[0]] == $l1_bauritu[0]){
					$s_rand =int(rand($#sutetasu_name + 1));
					$s_name = $sutetasu_name[$s_rand];
					&sutetasu_up("$s_name","$sute_bai");
					$coment .= "$s_name+$sute_bai<br>";
				}else{
					$atare_d = $in{'rate'} * $l1_bauritu[$liru1[0]];
					$atarikane += $atare_d;
					$disp .= "$in{'rate'}×$l1_bauritu[$liru1[0]] = $atare_d<br>";
				}
			}else{
				$atare_d = $in{'rate'} * $l1_bauritu[$liru1[0]];
				$atarikane += $atare_d;
				$disp .= "$in{'rate'}×$l1_bauritu[$liru1[0]] = $atare_d<br>";
			}
		}
		if($liru1[2] == $liru2[1] && $liru2[1] ==$liru3[0]){
			if ($sutetasu_on eq 'yes'){
				if ($l1_bauritu[$liru1[2]] == $l1_bauritu[0]){
					$s_rand =int(rand($#sutetasu_name + 1));
					$s_name = $sutetasu_name[$s_rand];
					&sutetasu_up("$s_name","$sute_bai");
					$coment .= "$s_name+$sute_bai<br>";
				}else{
					$atare_d = $in{'rate'} * $l1_bauritu[$liru1[2]];
					$atarikane += $atare_d;
					$disp .= "$in{'rate'}×$l1_bauritu[$liru1[2]] = $atare_d<br>";
				}
			}else{
				$atare_d = $in{'rate'} * $l1_bauritu[$liru1[2]];
				$atarikane += $atare_d;
				$disp .= "$in{'rate'}×$l1_bauritu[$liru1[2]] = $atare_d<br>";
			}
		}
# 3ライン追加
		if($liru1[0] == $liru1[1] && $liru1[1] ==$liru1[2]){
			if ($sutetasu_on eq 'yes'){
				if ($l1_bauritu[$liru1[0]] == $l1_bauritu[0]){
					$s_rand =int(rand($#sutetasu_name + 1));
					$s_name = $sutetasu_name[$s_rand];
					&sutetasu_up("$s_name","$sute_bai");
					$coment .= "$s_name+$sute_bai<br>";
				}else{
					$atare_d = $in{'rate'} * $l1_bauritu[$liru1[0]];
					$atarikane += $atare_d;
					$disp .= "$in{'rate'}×$l1_bauritu[$liru1[0]] = $atare_d<br>";
				}
			}else{
				$atare_d = $in{'rate'} * $l1_bauritu[$liru1[0]];
				$atarikane += $atare_d;
				$disp .= "$in{'rate'}×$l1_bauritu[$liru1[0]] = $atare_d<br>";
			}
		}

		if($liru2[0] == $liru2[1] && $liru2[1] ==$liru2[2]){
			if ($sutetasu_on eq 'yes'){
				if ($l1_bauritu[$liru2[0]] == $l1_bauritu[0]){
					$s_rand =int(rand($#sutetasu_name + 1));
					$s_name = $sutetasu_name[$s_rand];
					&sutetasu_up("$s_name","$sute_bai");
					$coment .= "$s_name+$sute_bai<br>";
				}else{
					$atare_d = $in{'rate'} * $l1_bauritu[$liru2[0]];
					$atarikane += $atare_d;
					$disp .= "$in{'rate'}×$l1_bauritu[$liru2[0]] = $atare_d<br>";
				}
			}else{
				$atare_d = $in{'rate'} * $l1_bauritu[$liru2[0]];
				$atarikane += $atare_d;
				$disp .= "$in{'rate'}×$l1_bauritu[$liru2[0]] = $atare_d<br>";
			}
		}

		if($liru3[0] == $liru3[1] && $liru3[1] ==$liru3[2]){  #修正
			if ($sutetasu_on eq 'yes'){
				if ($l1_bauritu[$liru3[0]] == $l1_bauritu[0]){
					$s_rand =int(rand($#sutetasu_name + 1));
					$s_name = $sutetasu_name[$s_rand];
					&sutetasu_up("$s_name","$sute_bai");
					$coment .= "$s_name+$sute_bai<br>";
				}else{
					$atare_d = $in{'rate'} * $l1_bauritu[$liru3[0]];
					$atarikane += $atare_d;
					$disp .= "$in{'rate'}×$l1_bauritu[$liru3[0]] = $atare_d<br>";
				}
			}else{
				$atare_d = $in{'rate'} * $l1_bauritu[$liru3[0]];
				$atarikane += $atare_d;
				$disp .= "$in{'rate'}×$l1_bauritu[$liru3[0]] = $atare_d<br>";
			}
		}

		#所持金変更処理
		#所持金　-　かけた金額　+　賞金
		if ($motokin_hiku eq 'yes'){
			$money = $money - $in{'rate'} + $atarikane;
			$coment2 = $coment;
			$coment2 =~ s/<br>/ /g;
			if ($atarikane != 0 || $coment){
				$atari="<font color=\"#ff0000\">あたりました～<BR>$disp $coment2総額$atarikane - $in{'rate'}円です。</font>";
			}else{
				if (!$disp && !$coment){
					$atari = 'はずれ';
				}
			}
		}else{
			if ($atarikane != 0 || $coment2){
				$money += $atarikane;
				$atari="<font color=\"#ff0000\">あたりました～<BR>$disp $coment2総額$atarikane円です。</font>";
			}else{
				$money -= $in{'rate'};
				if (!$disp){
					$atari = 'はずれ';
				}
			}
		}
		#個人データ更新
		&temp_routin;
		&log_kousin($my_log_file,$k_temp);
		#１ラインスロットのデータ更新
		$j_liru1 = join("=",@liru1);
		$j_liru2 = join("=",@liru2);
		$j_liru3 = join("=",@liru3);


		$l1_new_data0="$name<>$now_time<>$j_liru1<>$j_liru2<>$j_liru3<>$atarikane<>$in{'rate'}<>$coment2<>\n";
		
		unshift(@l1_data , $l1_new_data0);
		if ($#l1_data + 1 >= 20){$#l1_data = 20 - 1;}

		&lock;
		open(KB,">$l1_log")|| &error("Open Error : $l1_log");
		eval{ flock (KB, 2); };
		print KB @l1_data;
		close(KB);
		
		&unlock;
		
	}

	#説明文１
	$slot_mes="
	<P><font size=\"3\">8ラインスロット</font><br>掛け金を選択してスロットボタンをクリックして下さい。<BR>同じマークがそろったら掛け金×マークの倍率が払い戻されます。<br>同じ人が続けて";
	#説明文２（同じ人が出来るか）
	if($l1_set1==1){
		$slot_mes.="出来ます。";
		#説明文３（出来る場合は時間間隔の表示）
		if($l1_set2!=0){
			$slot_mes.="（$l1_set2秒間隔）";
		}
	}else{
	#説明文２＋（同じ人はできない）
		$slot_mes.="出来ません";
	}

	#掛け金表示処理
	$rate="<select name=rate>";
	foreach (@l1_stt3){
		$rat=$_;
		if($l1_ste4==1 ||($l1_ste4==0 && $rat <= $money)){
			#掛け金の表示部分でのカンマ表示処理
			if ($rat =~ /^[-+]?\d\d\d\d+/g) {
				for ($i = pos($rat) - 3, $j = $rat =~ /^[-+]/; $i > $j; $i -= 3) {
					substr($rat, $i, 0) = ',';
				}
			}
			$rate.="<option value=$_>$rat</option>\n";
		}else{
			last;
		}
	}
	$rate.="</select>";

	(@liru1) = split(/=/, $j_liru1);
	(@liru2) = split(/=/, $j_liru2);
	(@liru3) = split(/=/, $j_liru3);
	print <<"EOM";
<table border="1" align=center class=yosumi width="80%">
<TD align=center>
$slot_mes<br><br>
<table border="1"  align=center class=yosumi>
<tr>
<TD><img src=$l1_img$liru1[0].gif></TD>
<TD><img src=$l1_img$liru2[0].gif></TD>
<TD><img src=$l1_img$liru3[0].gif></TD>
</tr><tr>
<TD><img src=$l1_img$liru1[1].gif></TD>
<TD><img src=$l1_img$liru2[1].gif></TD>
<TD><img src=$l1_img$liru3[1].gif></TD>
</tr><tr>
<TD><img src=$l1_img$liru1[2].gif></TD>
<TD><img src=$l1_img$liru2[2].gif></TD>
<TD><img src=$l1_img$liru3[2].gif></TD>
</tr>
</table><br>
現在の所持金：$money円<BR>
$coment $atari<br>
EOM
	if($money > 0){
		print <<"EOM";
<form method=\"POST\" action="$this_script">
<input type=hidden name=gamerand value="$in{'gamerand'}">
<input type=hidden name=mode value="l1_slot">
<input type=hidden name=command value="slot_ok">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=town_no value="$in{'town_no'}">
$rate
<input type=submit value=" スロット ">
</form></center>
</TD>
EOM
	}
	print <<"EOM";
<TD ALIGN=left VALIGN=top>
<table border="1" align=center class=yosumi>
EOM
	$x=0;
	foreach(@l1_bauritu){
		print <<"EOM";
<TR><TD><img src=$l1_img$x.gif></TD><TD><img src=$l1_img$x.gif></TD><TD><img src=$l1_img$x.gif></TD><TD>×$_</TD></TR>
EOM
		$x++;
	}
	print <<"EOM";
</table></table>
EOM

	print '<table border="1" align=center class=yosumi width="80%">';
	print "<tr><TD>■最近のゲーム<br>\n";
	foreach (@l1_data){
		($l1_name_d,$l1_time_d,$j_liru1,$j_liru2,$j_liru3,$atare_d,$in_rate,$coment2) = split(/<>/);
#koko 2005/05/11
		if ($motokin_hiku eq 'yes'){
			$shyokin = $atare_d- $in_rate;
			$disp_hiku = " - $in_rate = $shyokin";
		}
		if ($atare_d ==0){
			$coment1 = "<font color=\"#ff0000\">-$in_rate円</font>";
		}else{
			$coment1 = "$atare_d$disp_hiku円";
		}
		if ($atare_d != 0 || $coment2){ #あたりの時
			if ($atare_d / $in_rate >= 200){ #200倍以上の時
				print "<font color=\"#008000\"><b>$l1_name_dさんが$in_rate円掛けて $coment2$coment1です。大当たり。</b></font><br>\n";
			}else{
				print "<font color=\"#008000\"> $l1_name_dさんが$in_rate円掛けて $coment2$coment1です。</font><br>\n";
			}
		}else{
			print "<font color=\"#ff0000\"> $l1_name_dさんが$in_rate円掛けてはずれでした。</font><br>\n";
		}
#kokoend
	}
	print '</TD></tr></table>';
	print "<div align=\"right\">オリジナル:ゆかにゃん<br>Edit:たっちゃん<div>\n";
	&hooter("login_view","戻る");
	exit;
}
sub sutetasu_up{
	if ($_[0] eq "国語"){$kokugo += $_[1];}
	if ($_[0] eq "数学"){$suugaku += $_[1];}
	if ($_[0] eq "理科"){$rika += $_[1];}
	if ($_[0] eq "社会"){$syakai += $_[1];}
	if ($_[0] eq "英語"){$eigo += $_[1];}
	if ($_[0] eq "音楽"){$ongaku += $_[1];}
	if ($_[0] eq "美術"){$bijutu += $_[1];}
	if ($_[0] eq "ルックス"){$looks += $_[1];}
	if ($_[0] eq "体力"){$tairyoku += $_[1];}
	if ($_[0] eq "健康"){$kenkou += $_[1];}
	if ($_[0] eq "スピード"){$speed += $_[1];}
	if ($_[0] eq "パワー"){$power += $_[1];}
	if ($_[0] eq "腕力"){$wanryoku += $_[1];}
	if ($_[0] eq "脚力"){$kyakuryoku += $_[1];}
	if ($_[0] eq "love"){$love += $_[1];}
	if ($_[0] eq "面白さ"){$unique += $_[1];}
	if ($_[0] eq "Ｈ"){$etti += $_[1];}
}

##### くじ引き　0 以上 $_[0] 以下の数字を $_[1] 個選び返す
sub randcheck {
	my @list = ();
	my $str = "";
	my $i = 0;
	while ($i < $_[1]) {
		my $tmp = int(rand(($_[0])+1));
		if (index($str, $tmp) < 0) {
			$str .= ",$tmp";
			$i++;
		}
	}
	@list = split /,/,$str;
	shift(@list);	# 先頭の空要素取り除き
	return (@list);
}

