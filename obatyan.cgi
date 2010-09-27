#!/usr/bin/perl
# ↑お使いのサーバーのパスに合わせてください。

$this_script = 'obatyan.cgi';
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
	if($in{'mode'} eq "battle"){&battle;}
	elsif($in{'mode'} eq "strong"){&strong;}
	elsif($in{'mode'} eq "week"){&week;}
	else{&error("「戻る」ボタンで街に戻ってください");}
exit;
	
############################
#member/osaka/*log.cgi
#と
#dat_dir/obatyan.cgi
#を合わせる
#############以下サブルーチン

sub strong {
$oba_power = 'strong';
&battle
}
sub week {
$oba_power = 'week';
&battle
}
sub battle {
	if ($aite_id eq "$k_id"){&message("おばちゃんは逃げてしまったｗｗ","login_view");}
if($oba_power eq "week"){
	$aite_id = int(rand(5))+1;
	&weekobalog ($aite_id);
	$kakeru_money = 300;#×回数（×５）が減る（増える）
}elsif($oba_power eq "strong"){
	$aite_id = int(rand(5))+1;
	&strongobalog ($aite_id);
	$kakeru_money = 1000;#×回数（×５）が減る（増える）
#	}else{
#	$aite_id = int(rand(9))+1;
#	&weekobalog ($aite_id);
#	$kakeru_money = 1000;#×回数（×５）が減る（増える）
	}
	
	$aite_energy_max = int(($aite_looks/12) + ($aite_tairyoku/4) + ($aite_kenkou/4) + ($aite_speed/8) + ($aite_power/8) + ($aite_wanryoku/8) + ($aite_kyakuryoku/8));
	$aite_nou_energy_max = int(($aite_kokugo/6) + ($aite_suugaku/6) + ($aite_rika/6) + ($aite_syakai/6) + ($aite_eigo/6)+ ($aite_ongaku/6)+ ($aite_bijutu/6));
#アイコンがあれば代入
	if ($kounyuu){$icon_hyouzi_a = "<img src=$kounyuu width=32 height=32 align=left>";}else{$icon_hyouzi_a = "";}
	if ($aite_kounyuu){$aite_icon_hyouzi_a = "<img src=$aite_kounyuu width=32 height=32 align=left>";}else{$aite_icon_hyouzi_a = "";}
	&header;
	print <<"EOM";
	<br><br><table width="600" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr align=center><td>
<table border="0"  cellspacing="0" cellpadding="1" style=" border: $st_win_wak; border-style: solid; border-width: 1px;"  width=150>
<tr><td align=center colspan=2 bgcolor=#ccff66 >
$icon_hyouzi_a$name
</td></tr>
<tr><td align=right><span class=honbun3>頭脳パワー</span>：</td><td>$nou_energy</td></tr>
<tr><td align=right><span class=honbun3>身体パワー</span>：</td><td>$energy</td></tr>
<tr>
<tr style=" border: $st_win_wak; border-style: solid; border-top-width: 1px; border-right-width: 0px; border-bottom-width: 0px; border-left-width: 0px">
<td align=center><span class=tyuu colspan=2>頭　脳</span></td></tr>
<tr><td align=right><span class=honbun3>国語</span>：</td><td>$kokugo</td></tr>
<tr><td align=right><span class=honbun3>数学</span>：</td><td>$suugaku</td></tr>
<tr><td align=right><span class=honbun3>理科</span>：</td><td>$rika</td></tr>
<tr><td align=right><span class=honbun3>社会</span>：</td><td>$syakai</td></tr>
<tr><td align=right><span class=honbun3>英語</span>：</td><td>$eigo</td></tr>
<tr><td align=right><span class=honbun3>音楽</span>：</td><td>$ongaku</td></tr>
<tr><td align=right><span class=honbun3>美術</span>：</td><td>$bijutu</td></tr>
<tr style=" border: $st_win_wak; border-style: solid; border-top-width: 1px; border-right-width: 0px; border-bottom-width: 0px; border-left-width: 0px">
<td  colspan=2 align=center><span class=tyuu>身　体</span></td></tr>
<tr><td  align=right nowrap><span class=honbun3>ルックス</span>：</td><td>$looks</td></tr>
<tr><td align=right><span class=honbun3>体力</span>：</td><td>$tairyoku</td></tr>
<tr><td align=right><span class=honbun3>健康</span>：</td><td>$kenkou</td></tr>
<tr><td align=right nowrap><span class=honbun3>スピード</span>：</td><td>$speed</td></tr>
<tr><td align=right><span class=honbun3>パワー</span>：</td><td>$power</td></tr>
<tr><td align=right><span class=honbun3>腕力</span>：</td><td>$wanryoku</td></tr>
<tr><td align=right><span class=honbun3>脚力</span>：</td><td>$kyakuryoku</td></tr>
<tr style=" border: $st_win_wak; border-style: solid; border-top-width: 1px; border-right-width: 0px; border-bottom-width: 0px; border-left-width: 0px">
<td  colspan=2 align=center><span class=tyuu>その他</span></td>
<tr><td align=right><span class=honbun3>LOVE</span>：</td><td>$love</td></tr>
<tr><td align=right><span class=honbun3>面白さ</span>：</td><td>$unique</td></tr>
<tr><td align=right><span class=honbun3>エッチ</span>：</td><td>$etti</td></tr>
</table>
	</td><td>
	<div class=tyuu>$aite_nameと街で出会った！</div><br><br>
	<div class=dai>Fight start !!</div>
	</td><td>
<table border="0"  cellspacing="0" cellpadding="1" style=" border: $st_win_wak; border-style: solid; border-width: 1px;"  width=150>
<tr><td align=center colspan=2 bgcolor=#ffcc99>
$aite_icon_hyouzi_a$aite_name
</td></tr>
<tr><td align=right><span class=honbun3>頭脳パワー</span>：</td><td>$aite_nou_energy_max</td></tr>
<tr><td align=right><span class=honbun3>身体パワー</span>：</td><td>$aite_energy_max</td></tr>
<tr style=" border: $st_win_wak; border-style: solid; border-top-width: 1px; border-right-width: 0px; border-bottom-width: 0px; border-left-width: 0px">
<td colspan=2 align=center><span class=tyuu>頭　脳</span></td></tr>
<tr><td align=right><span class=honbun3>国語</span>：</td><td>$aite_kokugo</td></tr>
<tr><td align=right><span class=honbun3>数学</span>：</td><td>$aite_suugaku</td></tr>
<tr><td align=right><span class=honbun3>理科</span>：</td><td>$aite_rika</td></tr>
<tr><td align=right><span class=honbun3>社会</span>：</td><td>$aite_syakai</td></tr>
<tr><td align=right><span class=honbun3>英語</span>：</td><td>$aite_eigo</td></tr>
<tr><td align=right><span class=honbun3>音楽</span>：</td><td>$aite_ongaku</td></tr>
<tr><td align=right><span class=honbun3>美術</span>：</td><td>$aite_bijutu</td></tr>
<tr style=" border: $st_win_wak; border-style: solid; border-top-width: 1px; border-right-width: 0px; border-bottom-width: 0px; border-left-width: 0px">
<td  colspan=2 align=center><span class=tyuu>身　体</span></td></tr>
<tr><td  align=right nowrap><span class=honbun3>ルックス</span>：</td><td>$aite_looks</td></tr>
<tr><td align=right><span class=honbun3>体力</span>：</td><td>$aite_tairyoku</td></tr>
<tr><td align=right><span class=honbun3>健康</span>：</td><td>$aite_kenkou</td></tr>
<tr><td align=right nowrap><span class=honbun3>スピード</span>：</td><td>$aite_speed</td></tr>
<tr><td align=right><span class=honbun3>パワー</span>：</td><td>$aite_power</td></tr>
<tr><td align=right><span class=honbun3>腕力</span>：</td><td>$aite_wanryoku</td></tr>
<tr><td align=right><span class=honbun3>脚力</span>：</td><td>$aite_kyakuryoku</td></tr>
<tr style=" border: $st_win_wak; border-style: solid; border-top-width: 1px; border-right-width: 0px; border-bottom-width: 0px; border-left-width: 0px">
<td  colspan=2 align=center><span class=tyuu>その他</span></td>
<tr><td align=right><span class=honbun3>LOVE</span>：</td><td>$aite_love</td></tr>
<tr><td align=right><span class=honbun3>面白さ</span>：</td><td>$aite_unique</td></tr>
<tr><td align=right><span class=honbun3>エッチ</span>：</td><td>$aite_etti</td></tr>
</table>
	</td></tr></table>
EOM

	if ($speed > $aite_speed){$turn =1;}
	$sentou_kaisuu =0;
	foreach (1..50){
			print "<br><br><table width=\"600\" border=\"0\" cellspacing=\"0\" cellpadding=\"5\" align=center class=yosumi><tr><td colspan=2>";
			if ($turn == 1){&kougeki (1,$name);			#自分の攻撃
			}else{&kougeki (0,$aite_name);}			#相手の攻撃
			print <<"EOM";
			</td></tr>
			<tr><td align=left>
			<div class=tyuu>頭脳パワー：$nou_energy</div>
			<div class=tyuu>身体パワー：$energy</div>
			</td>
			<td align=right>
			<div class=tyuu>頭脳パワー：$aite_nou_energy_max</div>
			<div class=tyuu>身体パワー：$aite_energy_max</div>
			</td></tr></table>
EOM
			$sentou_kaisuu ++;
			if ($aite_energy_max <= 0){$win_flag=1;last;}
			if ($aite_nou_energy_max <= 0){$win_flag=2;last;}
			if ($energy <= 0){$win_flag=3;last;}
			if ($nou_energy <= 0){$win_flag=4;last;}
			if ($turn == 1){$turn = 0;} else {$turn = 1;}
	}
	print "<br><br>";
	if ($energy < 0){$energy = 0;}
	if ($nou_energy < 0){$nou_energy = 0;}
	$get_money=$sentou_kaisuu*$kakeru_money;
	if ($win_flag == 1) {
			$my_rand = int(rand(3));#準備して有る数
			&get_itm($my_rand);#0～準備して有る数-1
		$get_money *= 5;
			if($kensa_flag == 2){
		print "<div align=center style=\"color:#339933;font-size:14px;\">勝ちました！<br>倒れている$aite_nameの財布から<br>$get_money円とを奪いました。<br>持ち物が多くて物は奪えませんでした。</div>";
			}else{
		print "<div align=center style=\"color:#339933;font-size:14px;\">勝ちました！<br>倒れている$aite_nameの財布から<br>$get_money円と$syo_hinmoku0を奪いました。</div>";
			}
		$money += $get_money;
		
	}elsif($win_flag == 2){
			$my_rand = int(rand(3));#準備して有る数
			&get_itm($my_rand);#0～準備して有る数-1
		$get_money *= 5;
			if($kensa_flag == 2){
		print "<div align=center style=\"color:#339933;font-size:14px;\">勝ちました！<br>考える力のない$aite_nameの財布から<br>$get_money円とを奪いました。<br>持ち物が多くて物は奪えませんでした。</div>";
			}else{
		print "<div align=center style=\"color:#339933;font-size:14px;\">勝ちました！<br>考える力のない$aite_nameの財布から<br>$get_money円と$syo_hinmoku0を奪いました。</div>";
			}
		$money += $get_money;
		
	}elsif($win_flag == 3){
		print "<div align=center style=\"color:#ff3300;font-size:14px;\">負けてしまいました。。<br>ボロボロになった$nameの財布から<br>$get_money円を奪われました。</div>";
		$money -= $get_money;
	}elsif($win_flag == 4){
		print "<div align=center style=\"color:#ff3300;font-size:14px;\">負けてしまいました。。<br>意識がもうろうとした$nameの財布から<br>$get_money円を奪われました。</div>";
		$money -= $get_money;
	}else{
		print "決着がつきませんでした。。";
	}
#データ更新
			&temp_routin;
			&log_kousin($my_log_file,$k_temp);
	&hooter("login_view","戻る");
	exit;
}

sub kougeki {
#攻撃内容をランダムで選択
		$battle_rand = int(rand(16))+1;
		print "<table width=\"600\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\" align=center><tr align=center><td>";
##自分の攻撃の場合
		if (@_[0] == 1){
			print "<div style=\"color:#339933;font-size:12px;\" align=left>@_[1]の攻撃！<br>";
#攻撃内容
			&kougekinaiyou (1,$aite_name);
#結果表示
			if ($damage eq "no_d"){
					print "<div style=\"color:#ff3300;font-size:12px;\" align=right>$return_naiyou</div>\n";
			}else{
					print "<div style=\"color:#339933;font-size:12px;\" align=right>$return_naiyou</div>\n";
					if ($battle_rand <= 8 || $battle_rand == 14){
						$aite_nou_energy_max -= $damage;
					}else{
						$aite_energy_max -= $damage;
					}
			}
			
##相手の攻撃の場合
		}else {
			print "<div style=\"color:#ff3300;font-size:12px;\" align=right>@_[1]の攻撃！<br>";
			&kougekinaiyou (0,$name);
#結果表示
#自分にきかない場合
			if ($damage eq "no_d"){
					print "<div style=\"color:#339933;font-size:12px;\" align=left>$return_naiyou</div>\n";
			}else{
#ダメージを受けた場合
					print "<div style=\"color:#ff3300;font-size:12px;\" align=left>$return_naiyou</div>\n";
#頭脳ダメージ
					if ($battle_rand <= 8 || $battle_rand == 14){
						$nou_energy -= $damage;
					}else{
#肉体ダメージ
						$energy -= $damage;
					}
			}
		}
	print "</td></tr></table>";
}

###攻撃内容ごとのダメージ処理サブルーチン
sub kougekinaiyou {
# @_[0]＝1なら自分の攻撃、0なら相手の攻撃
	if (@_[0] == 1){$align_settei = "align=left";}else{$align_settei = "align=right";}
#国語の攻撃
		if ($battle_rand ==1){
			print "この漢字が読めるか？と@_[1]に歩み寄った！</div><br>\n";
# iryoku_hantei (攻撃者,攻撃の内容)
			&iryoku_hantei (@_[0],1);
			if ($damage eq "no_d"){$return_naiyou = "@_[1]は漢字が得意だったのであっさり答えた。。";}
			else{$return_naiyou = "「よ、読めない。。」@_[1]は <span style=\"font-size:18px\">$damage</span> の精神的ダメージを受けた！";}
		}

		if ($battle_rand ==2){
			print "難しい数学の問題で@_[1]を困らせようとした！</div><br>\n";
# iryoku_hantei (攻撃者,攻撃の内容)
			&iryoku_hantei (@_[0],2);
			if ($damage eq "no_d"){$return_naiyou = "@_[1]は数学が得意だったので効果が無かった。。";}
			else{$return_naiyou = "ちんぷんかんぷんだった@_[1]は <span style=\"font-size:18px\">$damage</span> の精神的ダメージを受けた！";}
		}

		if ($battle_rand ==3){
			print "理科の公式を唱えて@_[1]の動揺を誘った！</div><br>\n";
# iryoku_hantei (攻撃者,攻撃の内容)
			&iryoku_hantei (@_[0],3);
			if ($damage eq "no_d"){$return_naiyou = "@_[1]は理科が得意だったので効果が無かった。。";}
			else{$return_naiyou = "頭が混乱した@_[1]は <span style=\"font-size:18px\">$damage</span> の精神的ダメージを受けた！";}
		}

		if ($battle_rand ==4){
			print "有名な歴史の事件の年号を@_[1]に質問攻めした！</div><br>\n";
# iryoku_hantei (攻撃者,攻撃の内容)
			&iryoku_hantei (@_[0],4);
			if ($damage eq "no_d"){$return_naiyou = "@_[1]は歴史が大得意だった。。";}
			else{$return_naiyou = "焦った@_[1]は <span style=\"font-size:18px\">$damage</span> の精神的ダメージを受けた！";}
		}

		if ($battle_rand ==5){
			print "突然英語をしゃべり出した！</div><br>\n";
# iryoku_hantei (攻撃者,攻撃の内容)
			&iryoku_hantei (@_[0],5);
			if ($damage eq "no_d"){$return_naiyou = "@_[1]も負けじと英語で答えた。。";}
			else{$return_naiyou = "「もっと英語を勉強せねば。。」と@_[1]は <span style=\"font-size:18px\">$damage</span> の精神的ダメージを受けた！";}
		}

		if ($battle_rand ==6){
			print "近くにあったピアノの鍵盤を叩き、この音階は何？と質問した！</div><br>\n";
# iryoku_hantei (攻撃者,攻撃の内容)
			&iryoku_hantei (@_[0],6);
			if ($damage eq "no_d"){$return_naiyou = "@_[1]は簡単に質問に答えた。。";}
			else{$return_naiyou = "「わ、わからん。。」@_[1]は <span style=\"font-size:18px\">$damage</span> の精神的ダメージを受けた！";}
		}

		if ($battle_rand ==7){
			print "すらすらと景色を描いて@_[1]に見せた！</div><br>\n";
# iryoku_hantei (攻撃者,攻撃の内容)
			&iryoku_hantei (@_[0],7);
			if ($damage eq "no_d"){$return_naiyou = "@_[1]は「この下手くそが！」と吐き捨てた。。";}
			else{$return_naiyou = "「う、うまい。。」@_[1]は<span style=\"font-size:18px\">$damage</span> の精神的ダメージを受けた！";}
		}

		if ($battle_rand ==8){
			print "ルックスで勝負しろ！と@_[1]に迫った！</div><br>\n";
# iryoku_hantei (攻撃者,攻撃の内容)
			&iryoku_hantei (@_[0],8);
			if ($damage eq "no_d"){$return_naiyou = "@_[1]は「勝ったね」とつぶやいた。";}
			else{$return_naiyou = "「う。。」@_[1]は <span style=\"font-size:18px\">$damage</span> の精神的ダメージを受けた！";}
		}

		if ($battle_rand ==9){
			print "体力勝負に持ち込んだ</div><br>\n";
# iryoku_hantei (攻撃者,攻撃の内容)
			&iryoku_hantei (@_[0],9);
			if ($damage eq "no_d"){$return_naiyou = "@_[1]は体力に自信があった。。";}
			else{$return_naiyou = "@_[1]は<span style=\"font-size:18px\">$damage</span> の肉体的疲労を受けた！";}
		}

		if ($battle_rand ==10){
			print "素早いフットワークで@_[1]を翻弄しようとした！</div><br>\n";
# iryoku_hantei (攻撃者,攻撃の内容)
			&iryoku_hantei (@_[0],11);
			if ($damage eq "no_d"){$return_naiyou = "@_[1]の方が素早かった。。";}
			else{$return_naiyou = "@_[1]は翻弄され <span style=\"font-size:18px\">$damage</span> の肉体的疲労を受けた！";}
		}

		if ($battle_rand ==11){
			print "パワーで@_[1]を投げ飛ばそうとした！</div><br>\n";
# iryoku_hantei (攻撃者,攻撃の内容)
			&iryoku_hantei (@_[0],12);
			if ($damage eq "no_d"){$return_naiyou = "@_[1]はもっとパワーがあった。。";}
			else{$return_naiyou = "@_[1]は投げ飛ばされ <span style=\"font-size:18px\">$damage</span> の肉体的ダメージを受けた！";}
		}

		if ($battle_rand ==12){
			print "@_[1]にパンチを浴びせた！</div><br>\n";
# iryoku_hantei (攻撃者,攻撃の内容)
			&iryoku_hantei (@_[0],13);
			if ($damage eq "no_d"){$return_naiyou = "しかし@_[1]は軽くよけた。。";}
			else{$return_naiyou = "@_[1]は パンチを浴び<span style=\"font-size:18px\">$damage</span> の肉体的ダメージを受けた！";}
		}

		if ($battle_rand ==13){
			print "@_[1]に蹴りかかった！</div><br>\n";
# iryoku_hantei (攻撃者,攻撃の内容)
			&iryoku_hantei (@_[0],14);
			if ($damage eq "no_d"){$return_naiyou = "しかし@_[1]はさっとよけた。。";}
			else{$return_naiyou = "@_[1]は 蹴りを浴び<span style=\"font-size:18px\">$damage</span> の肉体的ダメージを受けた！";}
		}

		if ($battle_rand ==14){
			print "愛している恋人の自慢を始めた！</div><br>\n";
# iryoku_hantei (攻撃者,攻撃の内容)
			&iryoku_hantei (@_[0],15);
			if ($damage eq "no_d"){$return_naiyou = "@_[1]はもっと恋人を愛していると言った。。";}
			else{$return_naiyou = "「う、うらやましい。。」@_[1]は <span style=\"font-size:18px\">$damage</span> の精神的ダメージを受けた！";}
		}

		if ($battle_rand ==15){
			print "@_[1]を笑わせ、そのスキに一発おみまいしようとした！</div><br>\n";
# iryoku_hantei (攻撃者,攻撃の内容)
			&iryoku_hantei (@_[0],16);
			if ($damage eq "no_d"){$return_naiyou = "「つまらん！」と@_[1]は一蹴した。。";}
			else{$return_naiyou = "@_[1]は笑い転げ、その隙に <span style=\"font-size:18px\">$damage</span> のパンチをくらった！";}
		}
		
		if ($battle_rand ==16){
			print "日頃のエッチで培った秘密技を披露した！</div><br>\n";
# iryoku_hantei (攻撃者,攻撃の内容)
			&iryoku_hantei (@_[0],17);
			if ($damage eq "no_d"){$return_naiyou = "@_[1]の方が一枚うわてだった。。";}
			else{$return_naiyou = "@_[1]は翻弄され <span style=\"font-size:18px\">$damage</span> の肉体的ダメージを受けた！";}
		}
}

#威力判定サブルーチン
sub iryoku_hantei {
#攻撃の内容ごとの能力値
	$iryoku_hanteiti = @_[1] + 5;
	if (@_[0] == 1){
		$hantei_kakkati = $nouryoku_suuzi_hairetu[$iryoku_hanteiti]  - $aite_nouryoku_suuzi_hairetu[$iryoku_hanteiti] ;
	}else{
		$hantei_kakkati = $aite_nouryoku_suuzi_hairetu[$iryoku_hanteiti]  - $nouryoku_suuzi_hairetu[$iryoku_hanteiti] ;
	}
	if ($hantei_kakkati <= 0){
			$damage = "no_d";
	}else{
			$damage = "$hantei_kakkati";
	}
}

sub get_itm{
	$getitm = $_[0];
#	0=英文解釈教室 1=成り上がり 2=おばあちゃんの知恵袋 今はこれだけ　持ち物オーバーでも増えていきます。規制は入っていません。
if($oba_power eq "week"){
	@plazentitm =(
'ゲットアイテム<>おばちゃんの力<>0<>0<>0<>0<>0<>0<>0<>無3<>3<>3<>3<>3<>3<>3<>0<>3<>3<>3<><>3<>回<>30<>5<>0<><><>10<><>0<>0<>0<>\n'
,'ゲットアイテム<>関西弁翻訳機<>3<>3<>3<>3<>3<>3<>3<>無<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>3<>回<>30<>15<>0<><><>3<><>0<>0<>0<>\n'
,'ゲットアイテム<>おばちゃんの知恵薬<>3<>3<>3<>3<>3<>3<>3<>万能,15<>3<>3<>3<>3<>3<>3<>3<>0<>3<>3<>3<>3<>回<>30<>5<>0<><><>10<><>0<>0<>0<>\n'
,'ゲットアイテム<>おばちゃんの知恵袋<>5<>5<>5<>5<>5<>5<>5<>無<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>3<>回<>30<>5<>0<><><>10<><>0<>0<>0<>\n'
);
}else{
	@plazentitm =(
'ゲットアイテム<>おばちゃんの力<>0<>0<>0<>0<>0<>0<>0<>10<>10<>10<>10<>10<>10<>10<>0<>10<>10<>10<>5<>回<>30<>5<>0<><><>10<><>0<>0<>0<>\n'
,'ゲットアイテム<>関西弁翻訳機<>10<>10<>10<>10<>10<>10<>10<>無<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>5<>回<>30<>15<>0<><><>3<><>0<>0<>0<>\n'
,'ゲットアイテム<>おばちゃんの知恵薬（スーパー）<>10<>10<>10<>10<>10<>10<>10<>万能,20<>10<>10<>10<>10<>10<>10<>10<>0<>10<>10<>10<>5<>回<>20<>10<>0<><><><><>0<>0<>0<>\n'
,'ゲットアイテム<>おばちゃんの知恵袋（スーパー）<>25<>25<>25<>25<>25<>25<>25<>無<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>5<>回<>30<>5<>0<><><>10<><>0<>0<>0<>\n'
);
}
	if ($#plazentitm < $getitm){&error("その品物は準備されていません。");}

	$monokiroku_file="./member/$k_id/mono.cgi";
	if (! -e $monokiroku_file){open (OUT,">$monokiroku_file") || &error("自分の購入物ファイルを作成できません");}
	close(OUT);
	open(OUT,"< $monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); };
	@my_kounyuu_list =<OUT>;
	close(OUT);

	if (@my_kounyuu_list >= $syoyuu_gendosuu){$kensa_flag=2;return;} # 持ち物オーバーで検査フラグを立てて帰る。


	($syo_syubetu0,$syo_hinmoku0,$syo_kokugo0,$syo_suugaku0,$syo_rika0,$syo_syakai0,$syo_eigo0,$syo_ongaku0,$syo_bijutu0,$syo_kouka0,$syo_looks0,$syo_tairyoku0,$syo_kenkou0,$syo_speed0,$syo_power0,$syo_wanryoku0,$syo_kyakuryoku0,$syo_nedan0,$syo_love0,$syo_unique0,$syo_etti0,$syo_taikyuu0,$syo_taikyuu_tani0,$syo_kankaku0,$syo_zaiko0,$syo_cal0,$syo_siyou_date0,$syo_sintai_syouhi0,$syo_zunou_syouhi0,$syo_comment0,$syo_kounyuubi0,$tanka0,$tokubai)= split(/<>/,$plazentitm[$getitm]);

	$kensa_flag=0;
	@new_myitem_hairetu = ();
	foreach $one_kounyuu_item (@my_kounyuu_list){
		&syouhin_sprit ($one_kounyuu_item);
		if ($syo_syubetu eq $syo_syubetu0 && $syo_hinmoku eq $syo_hinmoku0){
			$syo_taikyuu += $syo_taikyuu0;
			$kensa_flag = 1;
		}
		&syouhin_temp;
		push @new_myitem_hairetu,$syo_temp;
	}
	if ($kensa_flag != 1){
		$syo_kounyuubi0 = time;
		$syo_temp0="$syo_syubetu0<>$syo_hinmoku0<>$syo_kokugo0<>$syo_suugaku0<>$syo_rika0<>$syo_syakai0<>$syo_eigo0<>$syo_ongaku0<>$syo_bijutu0<>$syo_kouka0<>$syo_looks0<>$syo_tairyoku0<>$syo_kenkou0<>$syo_speed0<>$syo_power0<>$syo_wanryoku0<>$syo_kyakuryoku0<>$syo_nedan0<>$syo_love0<>$syo_unique0<>$syo_etti0<>$syo_taikyuu0<>$syo_taikyuu_tani0<>$syo_kankaku0<>$syo_zaiko0<>$syo_cal0<>$syo_siyou_date0<>$syo_sintai_syouhi0<>$syo_zunou_syouhi0<>$syo_comment0<>$syo_kounyuubi0<>$tanka0<>$tokubai0<>\n";
		push @new_myitem_hairetu,$syo_temp0;
	}
	open(OUT,">$monokiroku_file") || &error("Write Error : $monokiroku_file");
	eval{ flock (OUT, 2); };
	print OUT @new_myitem_hairetu;
	close(OUT);	
}