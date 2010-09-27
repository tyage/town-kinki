#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。
#################################
# 歓迎メッセージ用　設定
# 送り先管理者のID番号
$kanrisya_id = "1";
# 送り先管理者名前。レスしても届くように登録してある名前を書いてください。
$kanrisyaname = '';
# 歓迎コメント
$m_comment = '';
# 入室合言葉
$in_aikotoba = '';
# ランダム紹介者処理# 'yes';'no';'';の三種類 #2/2 town_maker.cgi にもう一個。
$syokai = 'yes';
# 紹介者に紹介料の支払い。#koko2007/09/20
$syoukai_majin = 'yes';
# eval{ flock (IN, 2); }; 2007/06/19
#################################

$this_script = 'game.cgi';
require './town_ini.cgi';
require './town_lib.pl';
require './event.pl';
&decode;
#メンテチェック
	if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}
$seigenyou_now_time = time;
#制限時間チェック
		$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
		if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。")}
		
#条件分岐
    if($in{'mode'} eq "battle"){&battle;}
	elsif($in{'mode'} eq "doukyo"){&doukyo;}
	elsif($in{'mode'} eq "c_league"){&c_league;}
	elsif($in{'mode'} eq "new_hyouji"){&new_hyouji;}
	elsif($in{'mode'} eq "new"){&new;}
	elsif($in{'mode'} eq "data_hozon"){&data_hozon;}
	else{&error("「戻る」ボタンで街に戻ってください");}
exit;
	
#############以下サブルーチン
sub battle {
	open(IN,"< $logfile") || &error("Open Error : $logfile");
	eval{ flock (IN, 2); };
	@aite_erabi = <IN>;
	close(IN);
#	srand(time^$$);
	$randed= int (rand($#aite_erabi));
	$aite_erabi=splice(@aite_erabi,$randed,1);
	($aite_id) = split(/<>/,$aite_erabi);
	if ($aite_id eq "$k_id"){&message("闘う相手が見つからなかった。。","login_view");}
	&openAitelog ($aite_id);
	
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
$icon_hyouzi_a$nameさん
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
	<div class=tyuu>$aite_nameさんと街で出会った！</div><br><br>
	<div class=dai>Fight start !!</div>
	</td><td>
<table border="0"  cellspacing="0" cellpadding="1" style=" border: $st_win_wak; border-style: solid; border-width: 1px;"  width=150>
<tr><td align=center colspan=2 bgcolor=#ffcc99>
$aite_icon_hyouzi_a$aite_nameさん
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
	$get_money=$sentou_kaisuu*300;
	if ($win_flag == 1) {
	
		$get_money *= 5;
		print "<div align=center style=\"color:#339933;font-size:14px;\">勝ちました！<br>倒れている$aite_nameさんの財布から<br>$get_money円を奪いました。</div>";
		$money += $get_money;
	if (int(rand(10))+1 == 1){
			$coupon_rand2 = int(rand(5))+1;
		&coupon_get($coupon_rand2);
		print "<br><div align=center style=\"color:#339933;font-size:14px;\">★クーポン券を$coupon_rand2枚もらいました！</div>";
		}
		
	}elsif($win_flag == 2){
	
		$get_money *= 5;
		print "<div align=center style=\"color:#339933;font-size:14px;\">勝ちました！<br>考える力の無い$aite_nameさんの財布から<br>$get_money円を奪いました。</div>";
		$money += $get_money;
		if (int(rand(10))+1 == 1){
		   $coupon_rand2 = int(rand(5))+1;
		   &coupon_get($coupon_rand2);
		   print "<br><div align=center style=\"color:#339933;font-size:14px;\">★クーポン券を$coupon_rand2枚もらいました！</div>";
		}
		
	}elsif($win_flag == 3){
		print "<div align=center style=\"color:#ff3300;font-size:14px;\">負けてしまいました。。<br>ボロボロになった$nameさんの財布から<br>$get_money円を奪われました。</div>";
		$money -= $get_money;
	}elsif($win_flag == 4){
		print "<div align=center style=\"color:#ff3300;font-size:14px;\">負けてしまいました。。<br>意識がもうろうとした$nameさんの財布から<br>$get_money円を奪われました。</div>";
		$money -= $get_money;
	}else{
		print "決着がつきませんでした。。";
	}
	if(int(rand(10))+1 == 1){
	   $kpoint -= 3;
	   print "<br><div align=center style=\"color:#339933;font-size:14px;\">☆おっと！警察に見つかってしまった！Ｋポイント３Ｐがさがってしまった。。。</div>";
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

####同居人
sub doukyo {
		if ($chara_x_size == "" && $chara_y_size == ""){
			$chara_gazou_size = "";
			$c_size_comment = "";
		}else{
			$chara_gazou_size = "width=$chara_x_size height=$chara_y_size";
			$c_size_comment = "画像サイズは横$chara_x_sizeピクセル、縦$chara_y_sizeピクセルです。";
		}
		$chara_settei_file="./member/$k_id/chara_ini.cgi";
			if (! -e $chara_settei_file){
				open(OIB,">$chara_settei_file") || &error("Write Error : $chara_settei_file");
				eval{ flock (OIB, 2); };
				chmod 0666,"$chara_settei_file";
				close(OIB);
			}
		open(CSF,"< $chara_settei_file") || &error("Open Error : $chara_settei_file");
			$chara_settei_data = <CSF>;
			($ch_k_id,$ch_name,$ch_oyaname,$ch_gazou,$ch_point,$ch_yuusyoukai,$ch_kokugo,$ch_suugaku,$ch_rika,$ch_syakai,$ch_eigo,$ch_ongaku,$ch_bijutu,$ch_looks,$ch_tairyoku,$ch_kenkou,$ch_speed,$ch_power,$ch_wanryoku,$ch_kyakuryoku,$ch_love,$ch_unique,$ch_etti,$ch_energy,$ch_nou_energy,$ch_sintai,$ch_zunou,$ch_me_kokugo,$ch_me_suugaku,$ch_me_rika,$ch_me_syakai,$ch_me_eigo,$ch_me_ongaku,$ch_me_bijutu,$ch_me_looks,$ch_me_tairyoku,$ch_me_kenkou,$ch_me_speed,$ch_me_power,$ch_me_wanryoku,$ch_me_kyakuryoku,$ch_me_love,$ch_me_unique,$ch_me_etti,$ch_k_yobi3,$ch_k_yobi4,$ch_k_yobi5)= split(/<>/,$chara_settei_data);
		close(CSF);
		
#キャラ設定処理の場合
		if ($in{'command'} eq "make_chara"){
			if (length($in{'ch_name'}) > 30) {&error("キャラクターの名前は30字以内です");}
			$cgi_lib'maxdata = 51200;
			$MaxW = 80;	# 横幅
			$MaxH = 80;	# 縦幅
			if ($ch_k_id eq ""){$ch_k_id = $k_id;}
#koko2005/05/04
			if (!( $in{'ch_gazou'} =~ /http\:\/\/./) && $in{'ch_gazou'}){
				&error("http://で始まるアドレスを指定してください。");
			}else {
				$ch_gazou = $in{'ch_gazou'}; #位置空指定許可
			}
			if ($in{'ch_name'}){ 
				$ch_name = $in{'ch_name'};
				&c_ne_chra; #新しく作った
			}
#kokoend
			if ($ch_oyaname eq ""){$ch_oyaname = $name;}
			#if ($in{'ch_gazou'}){$ch_gazou = $in{'ch_gazou'};}
			if ($in{'ch_kokugo'} && $kokugo > $in{'ch_kokugo'}) { $ch_kokugo += $in{'ch_kokugo'}; $message_in .= "国語パラメータを$in{'ch_kokugo'}あげました。<br>"; $hikukane += $in{'ch_kokugo'}; $kokugo -=$in{'ch_kokugo'}; }
			if ($in{'ch_suugaku'} && $suugaku > $in{'ch_suugaku'}) { $ch_suugaku += $in{'ch_suugaku'}; $message_in .= "数学パラメータを$in{'ch_suugaku'}あげました。<br>"; $hikukane += $in{'ch_suugaku'}; $suugaku -=$in{'ch_suugaku'};}
			if ($in{'ch_rika'} && $rika > $in{'ch_rika'}) { $ch_rika += $in{'ch_rika'}; $message_in .= "理科パラメータを$in{'ch_rika'}あげました。<br>"; $hikukane += $in{'ch_rika'}; $rika -=$in{'ch_rika'};}
			if ($in{'ch_syakai'} && $syakai > $in{'ch_syakai'}) { $ch_syakai += $in{'ch_syakai'}; $message_in .= "社会パラメータを$in{'ch_rika'}あげました。<br>"; $hikukane += $in{'ch_syakai'}; $syakai -=$in{'ch_syakai'};}
			if ($in{'ch_eigo'} && $eigo > $in{'ch_eigo'}) { $ch_eigo += $in{'ch_eigo'}; $message_in .= "英語パラメータを$in{'ch_eigo'}あげました。<br>"; $hikukane += $in{'ch_eigo'}; $eigo -=$in{'ch_eigo'};}
			if ($in{'ch_ongaku'} && $ongaku > $in{'ch_ongaku'}) { $ch_ongaku += $in{'ch_ongaku'}; $message_in .= "音楽パラメータを$in{'ch_ongaku'}あげました。<br>"; $hikukane += $in{'ch_ongaku'}; $ongaku -=$in{'ch_ongaku'};}
			if ($in{'ch_bijutu'} && $bijutu > $in{'ch_bijutu'}) { $ch_bijutu += $in{'ch_bijutu'}; $message_in .= "美術パラメータを$in{'ch_bijutu'}あげました。<br>"; $hikukane += $in{'ch_bijutu'}; $bijutu -=$in{'ch_bijutu'};}
			if ($in{'ch_looks'} && $looks > $in{'ch_looks'}) { $ch_looks += $in{'ch_looks'}; $message_in .= "ルックスパラメータを$in{'ch_looks'}あげました。<br>"; $hikukane += $in{'ch_looks'}; $looks -=$in{'ch_looks'};}
			if ($in{'ch_tairyoku'} && $tairyoku > $in{'ch_tairyoku'}) { $ch_tairyoku += $in{'ch_tairyoku'}; $message_in .= "体力パラメータを$in{'ch_tairyoku'}あげました。<br>"; $hikukane += $in{'ch_tairyoku'}; $tairyoku -=$in{'ch_tairyoku'};}
			if ($in{'ch_kenkou'} && $kenkou > $in{'ch_kenkou'}) { $ch_kenkou += $in{'ch_kenkou'}; $message_in .= "健康パラメータを$in{'ch_kenkou'}あげました。<br>"; $hikukane += $in{'ch_kenkou'}; $kenkou -=$in{'ch_kenkou'};}
			if ($in{'ch_speed'} && $speed > $in{'ch_speed'}) { $ch_speed += $in{'ch_speed'}; $message_in .= "スピードパラメータを$in{'ch_speed'}あげました。<br>"; $hikukane += $in{'ch_speed'}; $speed -=$in{'ch_speed'};}
			if ($in{'ch_power'} && $power > $in{'ch_power'}) { $ch_power += $in{'ch_power'}; $message_in .= "パワーパラメータを$in{'ch_power'}あげました。<br>"; $hikukane += $in{'ch_power'}; $power -=$in{'ch_power'};}
			if ($in{'ch_wanryoku'} && $wanryoku > $in{'ch_wanryoku'}) { $ch_wanryoku += $in{'ch_wanryoku'}; $message_in .= "腕力パラメータを$in{'ch_wanryoku'}あげました。<br>"; $hikukane += $in{'ch_wanryoku'}; $wanryoku -=$in{'ch_wanryoku'};}
			if ($in{'ch_kyakuryoku'} && $kyakuryoku > $in{'ch_kyakuryoku'}) { $ch_kyakuryoku += $in{'ch_kyakuryoku'}; $message_in .= "脚力パラメータを$in{'ch_kyakuryoku'}あげました。<br>"; $hikukane += $in{'ch_kyakuryoku'}; $kyakuryoku -=$in{'ch_kyakuryoku'};}
			if ($in{'ch_love'} && $love > $in{'ch_love'}) { $ch_love += $in{'ch_love'}; $message_in .= "LOVEパラメータを$in{'ch_love'}あげました。<br>"; $hikukane += $in{'ch_love'}; $love -=$in{'ch_love'};}
			if ($in{'ch_unique'} && $unique > $in{'ch_unique'}) { $ch_unique += $in{'ch_unique'}; $message_in .= "面白さパラメータを$in{'ch_unique'}あげました。<br>"; $hikukane += $in{'ch_unique'}; $unique -=$in{'ch_unique'};}
			if ($in{'ch_etti'} && $etti > $in{'ch_etti'}) { $ch_etti += $in{'ch_etti'}; $message_in .= "エッチパラメータを$in{'ch_etti'}あげました。<br>"; $hikukane += $in{'ch_etti'}; $etti -=$in{'ch_etti'};}
			
			if($hikukane =~ /[^0-9]/){&error("数値が不適切です");}
			if ($hikukane < 0){&error("数値が不適切です");}
			if ($hikukane != 0){
				$message_in .= "$hikukane万円のお金がかかりました。<br>";
			}
#koko 2005/04/16
			$c_kane_bank = $hikukane*10000;
			if ($k_sousisan < $c_kane_bank){&error("総資産以上は使えません");}
			if ($in{'siharaihouhou'} ne "現金"){
				$bank -= $hikukane*10000;
				if ($c_kane_bank){ #koko 2005/05/05
					&kityou_syori("クレジット支払い（Ｃリーグ支払い）","$c_kane_bank","",$bank,"普");
				}
			}else{
				if ($money < $hikukane*10000){&error("お金が足りません");}
				$money -= $hikukane*10000;
			}
			#if ($money < $hikukane*10000){&error("お金が足りません");}
			#kokoend
			
			if ($in{'ch_me_kokugo'}) { $ch_me_kokugo = "$in{'ch_me_kokugo'}";}
			if ($in{'ch_me_suugaku'}) { $ch_me_suugaku = "$in{'ch_me_suugaku'}";}
			if ($in{'ch_me_rika'}) { $ch_me_rika = "$in{'ch_me_rika'}";}
			if ($in{'ch_me_syakai'}) { $ch_me_syakai = "$in{'ch_me_syakai'}";}
			if ($in{'ch_me_eigo'}) { $ch_me_eigo = "$in{'ch_me_eigo'}";}
			if ($in{'ch_me_ongaku'}) { $ch_me_ongaku = "$in{'ch_me_ongaku'}";}
			if ($in{'ch_me_bijutu'}) { $ch_me_bijutu = "$in{'ch_me_bijutu'}";}
			if ($in{'ch_me_looks'}) { $ch_me_looks = "$in{'ch_me_looks'}";}
			if ($in{'ch_me_tairyoku'}) { $ch_me_tairyoku = "$in{'ch_me_tairyoku'}";}
			if ($in{'ch_me_kenkou'}) { $ch_me_kenkou = "$in{'ch_me_kenkou'}";}
			if ($in{'ch_me_speed'}) { $ch_me_speed = "$in{'ch_me_speed'}";}
			if ($in{'ch_me_power'}) { $ch_me_power = "$in{'ch_me_power'}";}
			if ($in{'ch_me_wanryoku'}) { $ch_me_wanryoku = "$in{'ch_me_wanryoku'}";}
			if ($in{'ch_me_kyakuryoku'}) { $ch_me_kyakuryoku = "$in{'ch_me_kyakuryoku'}";}
			if ($in{'ch_me_love'}) { $ch_me_love = "$in{'ch_me_love'}";}
			if ($in{'ch_me_unique'}) { $ch_me_unique = "$in{'ch_me_unique'}";}
			if ($in{'ch_me_etti'}) { $ch_me_etti = "$in{'ch_me_etti'}";}
			if  ($message_in eq ""){$message_in .= "変更しました。";}

#			if ($in{'upfile'}) { &UpFile; }
#パワーのMAX値計算
	$ch_sintai = int(($ch_looks / 10) + ($ch_tairyoku / 10) + ($ch_kenkou / 10) + ($ch_speed / 10) + ($ch_power / 10) + ($ch_wanryoku / 10) + ($ch_kyakuryoku / 10)+ ($ch_etti / 10));
	$ch_zunou = int(($ch_kokugo / 10) + ($ch_suugaku / 10) + ($ch_rika / 10) + ($ch_syakai / 10) + ($ch_eigo / 10)+ ($ch_ongaku / 10)+ ($ch_bijutu / 10)+ ($ch_love / 10)+ ($ch_unique / 10));
	
			$make_ch_temp ="$ch_k_id<>$ch_name<>$ch_oyaname<>$ch_gazou<>$ch_point<>$ch_yuusyoukai<>$ch_kokugo<>$ch_suugaku<>$ch_rika<>$ch_syakai<>$ch_eigo<>$ch_ongaku<>$ch_bijutu<>$ch_looks<>$ch_tairyoku<>$ch_kenkou<>$ch_speed<>$ch_power<>$ch_wanryoku<>$ch_kyakuryoku<>$ch_love<>$ch_unique<>$ch_etti<>$ch_energy<>$ch_nou_energy<>$ch_sintai<>$ch_zunou<>$ch_me_kokugo<>$ch_me_suugaku<>$ch_me_rika<>$ch_me_syakai<>$ch_me_eigo<>$ch_me_ongaku<>$ch_me_bijutu<>$ch_me_looks<>$ch_me_tairyoku<>$ch_me_kenkou<>$ch_me_speed<>$ch_me_power<>$ch_me_wanryoku<>$ch_me_kyakuryoku<>$ch_me_love<>$ch_me_unique<>$ch_me_etti<>$ch_k_yobi3<>$ch_k_yobi4<>$ch_k_yobi5";
	&lock;
	open(MTLO,">$chara_settei_file") || &error("Write Error : $chara_settei_file");
	eval{ flock (MTLO, 2); };
	print MTLO $make_ch_temp;
	close(MTLO);
	&unlock;
#	$money -= $hikukane * 10000;#koko2005/04/16
	$k_sousisan = $money + $bank + $super_teiki - ($loan_nitigaku * $loan_kaisuu);#koko2005/04/16
					&temp_routin;
					&log_kousin($my_log_file,$k_temp);
	&message("$message_in","doukyo","game.cgi");
		}		#作成処理の場合の閉じ
	
#コメントの初期化
	if ($ch_me_kokugo eq ""){$ch_me_kokugo = "この漢字が読めるか？";}
	if ($ch_me_suugaku eq ""){$ch_me_suugaku = "この数学の答えがわかるか？";}
	if ($ch_me_rika eq ""){$ch_me_rika = "この公式を考えたのは誰か知ってるか？";}
	if ($ch_me_syakai eq ""){$ch_me_syakai = "この事件は何年に起きたか知ってるか？";}
	if ($ch_me_eigo eq ""){$ch_me_eigo = "この英単語の意味を知ってるか？";}
	if ($ch_me_ongaku eq ""){$ch_me_ongaku = "この曲を作曲したのは誰か知ってるか？";}
	if ($ch_me_bijutu eq ""){$ch_me_bijutu = "この絵を見てみろ！";}
	if ($ch_me_looks eq ""){$ch_me_looks = "ルックスで勝負だ！";}
	if ($ch_me_tairyoku eq ""){$ch_me_tairyoku = "体力で勝負しろ！";}
	if ($ch_me_kenkou eq ""){$ch_me_kenkou = "健康には自信があるぞ！";}
	if ($ch_me_speed eq ""){$ch_me_speed = "このスピードについてこられるかな？";}
	if ($ch_me_power eq ""){$ch_me_power = "タックルで勝負だ！";}
	if ($ch_me_wanryoku eq ""){$ch_me_wanryoku = "腕相撲で勝負だ！";}
	if ($ch_me_kyakuryoku eq ""){$ch_me_kyakuryoku = "キックをお見舞いしてやる！";}
	if ($ch_me_love eq ""){$ch_me_love = "愛の深さでは負けないぞ！";}
	if ($ch_me_unique eq ""){$ch_me_unique = "このギャグどう？";}
	if ($ch_me_etti eq ""){$ch_me_etti = "エッチでは負けない！";}
#画面表示
		if ($ch_gazou){$charaimage_gazou = "<img src=$ch_gazou $chara_gazou_size>";}
		else{$charaimage_gazou = "";}
		&header(item_style);
		print <<"EOM";
	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr><td bgcolor=#ffffff>	
		ここでは自分だけのキャラクターを作成することができます。<br>
		キャラクターは自分のパラメーターとお金を投入することで成長します。<br>
		最強のキャラクターを作成して「Cリーグ」に参加しましょう。<br>
		（将来的には自分の家にキャラのコーナーができて来訪者とのやりとりができるようになる予\定です）<br>
	</td>
	<td bgcolor="#333333" align=center width=300><font color="#ffffff" size="5"><b>キャラクター</b></font></td>
	</tr></table><br>
EOM
	if ($in{'command'} eq ""){

#所有物チェック koko 2005/04/16
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(MK,"< $monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (MK, 2); };
	@my_kounyuu_list =<MK>;
	close(MK);
	foreach (@my_kounyuu_list){
		&syouhin_sprit ($_);
		if ($syo_kouka eq "クレジット"){
			if ($syo_taikyuu - (int ((time - $syo_kounyuubi) / (60*60*24)))){
				$siharai_houhou .= "<option value=\"$syo_hinmoku\">$syo_hinmoku</option>";
			}
		}
	}
	#kokoend

	print <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="doukyo">
	<input type=hidden name=command value="make_chara">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	
		<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
		<tr><td>
		<div align=center>
		$charaimage_gazou<br>
		<div class=honbun2>$ch_name</div><br>
		頭の良さ：$ch_zunou<br>
		身体能\力：$ch_sintai
		</div>
	
	</td><td>
	<div class=honbun2>●キャラの名前（全角15文字以内）</div>※随時変更ができます。<br>
	<input type=text size=30 name=ch_name value=$ch_name><br><br>
	
	<div class=honbun2>●キャラクター画像</div>（http://～で始まる絶対URL。$c_size_comment ※画像はなくても構\いません。）<br>※随時変更ができます。<br>
	<!--<input type=file name="upfile" size=30><br>-->
	<input type=text name="ch_gazou" size=60 value=$ch_gazou><br><br>
	
	<div class=honbun2>●パラメーターアップ</div>
	入力した数値分のパラメーターが自分から引かれ、さらにその数値×１万円の費用がかかります。<br>
	キャラクターは与えられた数値分のパラメーターが上がります。<br>
	<table border="0"><tr>
	<td>国語</td><td><input type=text name="ch_kokugo" size=10></td></td>
	<td>数学</td><td><input type=text name="ch_suugaku" size=10></td>
	<td>理科</td><td><input type=text name="ch_rika" size=10></td>
	<td>社会</td><td><input type=text name="ch_syakai" size=10></td>
	<td>英語</td><td><input type=text name="ch_eigo" size=10></td></tr><tr>
	<td>音楽</td><td><input type=text name="ch_ongaku" size=10></td>
	<td>美術</td><td><input type=text name="ch_bijutu" size=10></td>
	<td>ルックス</td><td><input type=text name="ch_looks" size=10></td>
	<td>体力</td><td><input type=text name="ch_tairyoku" size=10></td>
	<td>健康</td><td><input type=text name="ch_kenkou" size=10></td></tr><tr>
	<td>スピード</td><td><input type=text name="ch_speed" size=10></td>
	<td>パワー</td><td><input type=text name="ch_power" size=10></td>
	<td>腕力</td><td><input type=text name="ch_wanryoku" size=10></td>
	<td>脚力</td><td><input type=text name="ch_kyakuryoku" size=10></td>
	<td>LOVE</td><td><input type=text name="ch_love" size=10></td></tr><tr>
	<td>面白さ</td><td><input type=text name="ch_unique" size=10></td>
	<td>エッチ</td><td><input type=text name="ch_etti" size=10>
	</tr></table>

	</td><td width=150>
	<table border="0"  cellspacing="0" cellpadding="1" style=" border: $st_win_wak; border-style: solid; border-width: 1px;" bgcolor=#ffffcc width=100%>
<td colspan=2 align=center><span class=tyuu>頭　脳</span></td></tr>
<tr><td align=right><span class=honbun5>国語</span>：</td><td align=right>$ch_kokugo</td></tr>
<tr><td align=right><span class=honbun5>数学</span>：</td><td align=right>$ch_suugaku</td></tr>
<tr><td align=right><span class=honbun5>理科</span>：</td><td align=right>$ch_rika</td></tr>
<tr><td align=right><span class=honbun5>社会</span>：</td><td align=right>$ch_syakai</td></tr>
<tr><td align=right><span class=honbun5>英語</span>：</td><td align=right>$ch_eigo</td></tr>
<tr><td align=right><span class=honbun5>音楽</span>：</td><td align=right>$ch_ongaku</td></tr>
<tr><td align=right><span class=honbun5>美術</span>：</td><td align=right>$ch_bijutu</td></tr>
<tr style=" border: $st_win_wak; border-style: solid; border-top-width: 1px; border-right-width: 0px; border-bottom-width: 0px; border-left-width: 0px">
<td  colspan=2 align=center><span class=tyuu>身　体</span></td></tr>
<tr><td  align=right><span class=honbun5>ルックス</span>：</td><td align=right>$ch_looks</td></tr>
<tr><td align=right><span class=honbun5>体力</span>：</td><td align=right>$ch_tairyoku</td></tr>
<tr><td align=right><span class=honbun5>健康</span>：</td><td align=right>$ch_kenkou</td></tr>
<tr><td align=right><span class=honbun5>スピード</span>：</td><td align=right>$ch_speed</td></tr>
<tr><td align=right><span class=honbun5>パワー</span>：</td><td align=right>$ch_power</td></tr>
<tr><td align=right><span class=honbun5>腕力</span>：</td><td align=right>$ch_wanryoku</td></tr>
<tr><td align=right><span class=honbun5>脚力</span>：</td><td align=right>$ch_kyakuryoku</td></tr>
<tr style=" border: $st_win_wak; border-style: solid; border-top-width: 1px; border-right-width: 0px; border-bottom-width: 0px; border-left-width: 0px">
<td  colspan=2 align=center><span class=tyuu>その他</span></td>
<tr><td align=right><span class=honbun5>LOVE</span>：</td><td align=right>$ch_love</td></tr>
<tr><td align=right><span class=honbun5>面白さ</span>：</td><td align=right>$ch_unique</td></tr>
<tr><td align=right><span class=honbun5>エッチ</span>：</td><td align=right>$ch_etti</td></tr>
</table>
	</td></tr>
	<tr><td colspan=3>
	<div align=center>
支払い <select name="siharaihouhou">$siharai_houhou<option value="現金">現金</option></select><!-- koko -->

	<input type=submit value=" O K "></div>
	</td></tr></table>
	</form>
	
	<div align=center><form method="POST" action="$this_script">
	<input type=hidden name=mode value="doukyo">
	<input type=hidden name=command value="com_henkou">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="コメント変更フォーム出力"></form></div>
	
EOM
	}
	
	if ($in{'command'} eq "com_henkou"){
	print <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="doukyo">
	<input type=hidden name=command value="make_chara">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr><td>
	<div class=honbun2>●闘うときのコメント</div>
	各能\力ごとにその能\力で勝負する時に言うコメントを記入してください。※40字以内（このフォームの長さに収まるように）<br><br>
	<table border="0"><tr>
	<td>国語</td><td><input type=text name="ch_me_kokugo" size=80 value=$ch_me_kokugo></td></td></tr><tr>
	<td>数学</td><td><input type=text name="ch_me_suugaku" size=80 value=$ch_me_suugaku></td></tr><tr>
	<td>理科</td><td><input type=text name="ch_me_rika" size=80 value=$ch_me_rika></td></tr><tr>
	<td>社会</td><td><input type=text name="ch_me_syakai" size=80 value=$ch_me_syakai></td></tr><tr>
	<td>英語</td><td><input type=text name="ch_me_eigo" size=80 value=$ch_me_eigo></td></tr><tr>
	<td>音楽</td><td><input type=text name="ch_me_ongaku" size=80 value=$ch_me_ongaku></td></tr><tr>
	<td>美術</td><td><input type=text name="ch_me_bijutu" size=80 value=$ch_me_bijutu></td></tr><tr>
	<td>ルックス</td><td><input type=text name="ch_me_looks" size=80 value=$ch_me_looks></td></tr><tr>
	<td>体力</td><td><input type=text name="ch_me_tairyoku" size=80 value=$ch_me_tairyoku></td></tr><tr>
	<td>健康</td><td><input type=text name="ch_me_kenkou" size=80 value=$ch_me_kenkou></td></tr><tr>
	<td>スピード</td><td><input type=text name="ch_me_speed" size=80 value=$ch_me_speed></td></tr><tr>
	<td>パワー</td><td><input type=text name="ch_me_power" size=80 value=$ch_me_power></td></tr><tr>
	<td>腕力</td><td><input type=text name="ch_me_wanryoku" size=80 value=$ch_me_wanryoku></td></tr><tr>
	<td>脚力</td><td><input type=text name="ch_me_kyakuryoku" size=80 value=$ch_me_kyakuryoku></td></tr><tr>
	<td>LOVE</td><td><input type=text name="ch_me_love" size=80 value=$ch_me_love></td></tr><tr>
	<td>面白さ</td><td><input type=text name="ch_me_unique" size=80 value=$ch_me_unique></td></tr><tr>
	<td>エッチ</td><td><input type=text name="ch_me_etti" size=80 value=$ch_me_etti></td>
	</tr></table>
	<div align=center><input type=submit value=" コメント変更 "></div></form><br><br>
	<div align=center><a href="javascript:history.back()"> [前の画面に戻る] </a></div>
	</td></tr></table>
EOM
	}

	print <<"EOM";
	<center>
	<form method=POST action="game.cgi">
	<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>c_league<>">
	<input type=submit value="戻る">
	</form>
	</center>
EOM
		exit;
}
###キャラ違い　koko 2005/05/04
sub c_ne_chra{
	open(IN,"< $doukyo_logfile") || &error("Open Error : $doukyo_logfile");
	eval{ flock (IN, 2); };
	$league_meisai = <IN>;
	@aite_erabi = <IN>;
	close(IN);
	$i = 0;
	foreach (@aite_erabi){
		my ($ch_k_id,$ch_name0,$ch_oyaname,$ch_gazou0,$ch_kati,$ch_make,$ch_hikiwake,$ch_yuusyou,$ch_lasttime,$ch_yobi1,$ch_yobi2,$ch_yobi3,$ch_yobi4,$ch_yobi5,$ch_yobi6)= split(/<>/);
		if ($in{'name'} eq $ch_oyaname){
			$aite_erabi[$i] = "$ch_k_id<>$ch_name<>$ch_oyaname<>$ch_gazou<>$ch_kati<>$ch_make<>$ch_hikiwake<>$ch_yuusyou<>$ch_lasttime<>$ch_yobi1<>$ch_yobi2<>$ch_yobi3<>$ch_yobi4<>$ch_yobi5<>$ch_yobi6<>\n";
		}
		$i++;
	}

	@new_aite_erabi = @aite_erabi;
	unshift (@new_aite_erabi,$league_meisai);
	&lock;
	open(OUT,">$doukyo_logfile") || &error("Open Error : $doukyo_logfile");
	eval{ flock (OUT, 2); };
	print OUT @new_aite_erabi;
	close(OUT);			
	&unlock;
}
#kokoend

####Ｃリーグ
sub c_league {
		if ($chara_x_size == "" && $chara_y_size == ""){
			$chara_gazou_size = "";
			$c_size_comment = "";
		}else{
			$chara_gazou_size = "width=$chara_x_size height=$chara_y_size";
			$c_size_comment = "画像サイズは横$chara_x_sizeピクセル、縦$chara_y_sizeピクセルです。";
		}
		open(IN,"< $doukyo_logfile") || &error("Open Error : $doukyo_logfile");
		eval{ flock (IN, 2); };
		$league_meisai = <IN>;
		@aite_erabi = <IN>;
		close(IN);
		$now_time= time;
#ゲーム明細初期化
		if ($league_meisai eq ""){
			&lock;
			$league_meisai = "$now_time<>1<>\n";
			open(OUT,">$doukyo_logfile") || &error("Open Error : $doukyo_logfile");
			eval{ flock (OUT, 2); };
			print OUT $league_meisai;
			close(OUT);
			&unlock;
		}
		($start_time,$nankai_taikai)= split(/<>/,$league_meisai);
		$nannitime = int(($now_time - $start_time) / (60*60*24)) + 1;
		if ($nannitime > $c_nissuu){&taikai_syokika;}
		
#試合の場合
	if ($in{'command'}eq "game") {
		&lock;
#自分のキャラデータを開いて変数に入れる
	$chara_settei_file="./member/$k_id/chara_ini.cgi";
	open(CSF,"< $chara_settei_file") || &error("キャラを作成してからでないと試合はできません");
	eval{ flock (CSF, 2); };
	$chara_settei_data = <CSF>;
	@my_chara_para =  split(/<>/,$chara_settei_data);
	if ($chara_settei_data eq ""){&error("キャラを作成してからでないと試合はできません");}
	close(CSF);
#登録されているキャラIDで配列作成。未登録なら登録
	$zibun_hazusi = 0;
	@taisen_list = (); #koko2007/07/16
	@all_taisen_list = (); #koko2007/07/16
	foreach (@aite_erabi){
		($ch_k_id,$ch_name,$ch_oyaname,$ch_gazou,$ch_kati,$ch_make,$ch_hikiwake,$ch_yuusyou,$ch_lasttime)= split(/<>/);
#自分が見つかったら試合リストから自分をはずす。
		if(!(-e "./member/$ch_k_id/chara_ini.cgi")){next;} #koko2007/10/13
		if ($name eq $ch_oyaname){
			if ($now_time - $ch_lasttime < 60 * $c_siai_kankaku){&error("まだ前回の試合の疲れが残っています。");}
			$my_genzaino_joukyou = "$_";		#自分の状況を変数に入れておく
			$zibun_hazusi = 1;
			next;
		}
		push (@taisen_list,$ch_k_id);
		push (@all_taisen_list,$_);
	}
	if ($zibun_hazusi == 0){&c_league_touroku($chara_settei_data);}
	@nitteicheck = split(/<>/,$my_genzaino_joukyou);
	if ($nitteicheck[4] + $nitteicheck[5] + $nitteicheck[6] >= $c_siaisuu){&error("全試合日程を終了しています。");}
	$ch_randed=int(rand($#taisen_list));
	$aite_kettei =splice(@taisen_list,$ch_randed,1);
#koko2007/10/13
	if (0 == int(rand(3))){$aite_kettei = $k_id; $manera =1;}
#	if ($aite_kettei eq ""){&message("闘う相手が見つからなかった。。","login_view");}#koko 2005/04/17 c_league
	if ($aite_kettei eq ""){$aite_kettei = $k_id; $manera =1;}
#	if ($aite_kettei eq "$k_id"){&message("闘う相手が見つからなかった。。","login_view");}#koko 2005/04/17 c_league
#	if ($aite_kettei eq "$k_id"){$aite_kettei = $k_id; $manera =1;}#koko 2005/04/17 c_league koko2007/10/13
#相手のキャラデータを開いて変数に入れる
	$aite_settei_file="./member/$aite_kettei/chara_ini.cgi";
	if(!(-e $aite_settei_file)){$aite_settei_file="./member/$k_id/chara_ini.cgi"; $manera =1;}
#end2007/10/13
	open(ASF,"< $aite_settei_file") || &error("対戦相手の都合により試合は延期となりました/member/$aite_kettei/chara_ini.cgi。1");
	eval{ flock (ASF, 2); };
	$aite_settei_data = <ASF>;
	@aite_chara_para =  split(/<>/,$aite_settei_data);
	if ($aite_settei_data eq ""){&error("対戦相手の都合により試合は延期となりました。2");}
	close(ASF);
#キャラ画像があれば変数に代入
#koko2007/10/13
	if($manera){
		$aite_chara_para[1] = "まねらー$aite_chara_para[1]";
		$aite_chara_para[2] = "まねらー$aite_chara_para[2]";
	}
#end2007/10/13
	if ($my_chara_para[3]){
		$my_chara_image = "<img src=$my_chara_para[3] $chara_gazou_size>";
	}else{$my_chara_image = "";}
	if ($aite_chara_para[3]){
		$aite_chara_image = "<img src=$aite_chara_para[3] $chara_gazou_size>";
	}else{$aite_chara_image = "";}
	
	&header(item_style);
#キャラのパワー（体力）を算出
	$my_chara_power = $my_chara_para[26] + $my_chara_para[25];
	$aite_chara_power = $aite_chara_para[26] + $aite_chara_para[25];
	print <<"EOM";
	<br><br><table width="600" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr align=center><td>
<table border="0"  cellspacing="0" cellpadding="1" style=" border: $st_win_wak; border-style: solid; border-width: 1px;"  width=150>
<tr><td align=center colspan=2>
$my_chara_para[2]のキャラクター<br>
$my_chara_para[1]<br>
$my_chara_image
</td></tr>
<tr><td align=center><span class=honbun3>頭の良さ</span>：</td><td>$my_chara_para[26]</td></tr>
<tr><td align=center><span class=honbun3>身体能\力</span>：</td><td>$my_chara_para[25]</td></tr>
</table>
	</td><td>
	<div class=tyuu>$aite_chara_para[1]との試合が始まった！</div><br><br>
	</td><td>
<table border="0"  cellspacing="0" cellpadding="1" style=" border: $st_win_wak; border-style: solid; border-width: 1px;"  width=150>
<tr><td align=center colspan=2>
$aite_chara_para[2]のキャラクター<br>
$aite_chara_para[1]<br>
$aite_chara_image
</td></tr>
<tr><td align=center><span class=honbun3>頭の良さ</span>：</td><td>$aite_chara_para[26]</td></tr>
<tr><td align=center><span class=honbun3>身体能\力</span>：</td><td>$aite_chara_para[25]</td></tr>
</table>
	</td></tr></table>
EOM

	if ($my_chara_para[16] > $aite_chara_para[16]){$turn =1;}
	$sentou_kaisuu =0;
	foreach (1..25){
			print "<br><br><table width=\"600\" border=\"0\" cellspacing=\"0\" cellpadding=\"5\" align=center class=yosumi><tr><td colspan=2>";
			if ($turn == 1){&ch_kougeki (1,$my_chara_para[1]);			#自分の攻撃
			}else{&ch_kougeki (0,$aite_chara_para[1]);}			#相手の攻撃
			print <<"EOM";
			</td></tr>
			<tr><td align=left>
			<div class=tyuu>エネルギー：$my_chara_power</div>
			</td>
			<td align=right>
			<div class=tyuu>エネルギー：$aite_chara_power</div>
			</td></tr></table>
EOM
			$sentou_kaisuu ++;
			if ($aite_chara_power <= 0){$win_flag=1;last;}
			if ($my_chara_power <= 0){$win_flag=2;last;}
			if ($turn == 1){$turn = 0;} else {$turn = 1;}
	}
	print "<br><br>";
	
#先に入れておいた自分の状況をsplit
	($ch_k_id,$ch_name,$ch_oyaname,$ch_gazou,$ch_kati,$ch_make,$ch_hikiwake,$ch_yuusyou,$ch_lasttime,$ch_yobi1,$ch_yobi2,$ch_yobi3,$ch_yobi4,$ch_yobi5,$ch_yobi6)= split(/<>/,$my_genzaino_joukyou);
#ch_yobi1＝最後の対戦状況　ch_yobi2＝獲得ポイント　ch_yobi3＝前回勝ち　ch_yobi4＝前回負け　ch_yobi5＝前回引き分け

#勝った場合
	if ($win_flag == 1) {
		$ch_kati ++;
	#最後のバトルコメント
		$ch_yobi1 = "<td align=center>$my_chara_para[1] vs $aite_chara_para[1]</td><td align=center>$my_chara_para[1]</td><td>$my_chara_para[$battle_naiyou_hanbetu]</td>";
		print "<div align=center style=\"color:#339933;font-size:14px;\">見事勝利を収めました！</div>";
#koko 2005/04/17
		$c_mouke = $dameegitame * 2;
		if(!$c_mouke){$c_mouke = 100;}
		print "<div align=center style=\"color:#339933;font-size:14px;\">$c_mouke円手に入れた。</div>";
#kokoend
#負けた場合
	}elsif($win_flag == 2){
	#最後のバトルコメント
		$ch_yobi1 = "<td align=center>$my_chara_para[1] vs $aite_chara_para[1]</td><td align=center>$aite_chara_para[1]</td><td>$aite_chara_para[$battle_naiyou_hanbetu]</td>";
		$ch_make ++;
		print "<div align=center style=\"color:#ff3300;font-size:14px;\">負けてしまいました。。</div>";
#koko 2005/04/17
		$c_mouke = $dameegitame;
		if(!$c_mouke){$c_mouke = 100;}
		print "<div align=center style=\"color:#339933;font-size:14px;\">$c_mouke円手に入れた。</div>";
#kokoend
	}else{
		$ch_yobi1 = "<td align=center>$my_chara_para[1] vs $aite_chara_para[1]</td><td align=center>引き分け</td><td>ー</td>";
		$ch_hikiwake ++;
		print "<div align=center style=\"color:#ff3300;font-size:14px;\">決着がつきませんでした。。引き分けです。</div>";
#koko 2005/04/17
		$c_mouke = int($dameegitame * 1.5);
		if(!$c_mouke){$c_mouke = 100;}
		print "<div align=center style=\"color:#339933;font-size:14px;\">$c_mouke円手に入れた。</div>";
#kokoend
	}
	
	$ch_gazou ="$my_chara_para[3]";
	$ch_lasttime = $now_time;
	$c_sinki_temp = "$ch_k_id<>$ch_name<>$ch_oyaname<>$ch_gazou<>$ch_kati<>$ch_make<>$ch_hikiwake<>$ch_yuusyou<>$ch_lasttime<>$ch_yobi1<>$ch_yobi2<>$ch_yobi3<>$ch_yobi4<>$ch_yobi5<>$ch_yobi6<>\n"; 
	unshift (@all_taisen_list,$c_sinki_temp);
	unshift (@all_taisen_list,$league_meisai);
	open(TOO,">$doukyo_logfile") || &error("Open Error : $doukyo_logfile");
	eval{ flock (TOO, 2); };
	print TOO @all_taisen_list;
	close(TOO);
	&unlock;#koko 2005/04/17;抜けバグ
#koko 2005/04/17
	$money += $c_mouke;
#データ更新 
	&temp_routin;#&temp_routin;
	&log_kousin($my_log_file,$k_temp);#&log_kousin($my_log_file,$k_temp);
#kokoend
	&hooter("c_league","戻る","game.cgi");
	exit;
	}		#試合の場合の閉じ

		&header(keiba_style);
		print <<"EOM";
	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr><td bgcolor=#ffffff>
		最強のキャラクターを決める「Cリーグ」です。<br>
		$c_nissuu日間で$c_siaisuu試合を行うことができます。<br>
		もっとも勝利数の多いキャラクターが優勝となります。<br>
		試合間隔は$c_siai_kankaku分です。<br>
	</td>
	<td bgcolor="#333333" align=center width=300><font color="#ffffff" size="5"><b>Ｃリーグ</b></font></td>
	</tr></table><br>
		
		<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
		<tr><td>
EOM

	@alldata = (); #koko2007/07/16
	foreach (@aite_erabi){
		($ch_k_id,$ch_name,$ch_oyaname,$ch_gazou,$ch_kati,$ch_make,$ch_hikiwake,$ch_yuusyou,$ch_lasttime,$ch_yobi1,$ch_yobi2,$ch_yobi3,$ch_yobi4,$ch_yobi5,$ch_yobi6)= split(/<>/);
			if ($name eq $ch_oyaname){
				$my_genzaino_joukyou = "$_";		#自分の状況を変数に入れておく
			}
#koko2005/08/03		$key=(split(/<>/,$_))[4];		#ソートする要素を選ぶ
#			$key2=(split(/<>/,$_))[11];		#ソートする要素を選ぶ
#			$key3=(split(/<>/,$_))[10];		#ソートする要素を選ぶ
			push @alldata,$_;
#			push @keys,$key;
#			push @keys2,$key2;
#			push @keys3,$key3;
	}
	
#		sub bykeys{$keys[$b] <=> $keys[$a];}
#		@junidata=@alldata[ sort bykeys 0..$#alldata]; 
#
		@keys1 = map {(split /<>/)[4]} @alldata;
		@junidata = @alldata[sort {$keys1[$b] <=> $keys1[$a]} 0 .. $#keys1];
#		
#		sub bykeys3{$keys3[$b] <=> $keys3[$a];}
#		@sougoujunidata=@alldata[ sort bykeys3 0..$#alldata]; 
#
		@keys3 = map {(split /<>/)[10]} @alldata;
		@sougoujunidata = @alldata[sort {$keys3[$b] <=> $keys3[$a]} 0 .. $#keys3];
#		
#		sub bykeys2{$keys2[$b] <=> $keys2[$a];}
#		@zenkaijunidata=@alldata[ sort bykeys2 0..$#alldata]; 
#
		@keys2 = map {(split /<>/)[11]} @alldata;
		@zenkaijunidata = @alldata[sort {$keys2[$b] <=> $keys2[$a]} 0 .. $#keys2];
#kokoend

			($zibun_k_id,$zibun_name,$zibun_oyaname,$zibun_gazou,$zibun_kati,$zibun_make,$zibun_hikiwake) = split(/<>/,$my_genzaino_joukyou);
			if ($my_genzaino_joukyou ne ""){
				$syouhai_hyouzi = "『$zibun_name』は現在、$zibun_kati勝$zibun_make敗$zibun_hikiwake分け";
			}
	print <<"EOM";
	<div align=center class=dai>第$nankai_taikai回大会 - $nannitime日目 -</div>
	<div align=center>
	<form method=POST action="game.cgi">
    <input type=hidden name=mode value="doukyo">
    <input type=hidden name=name value="$in{'name'}">
    <input type=hidden name=pass value="$in{'pass'}">
    <input type=hidden name=k_id value="$k_id">
    <input type=hidden name=town_no value="$in{'town_no'}">
    <input type=submit value=キャラ育成></form>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="c_league">
	<input type=hidden name=command value="game">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value=試合をする></form>
	$syouhai_hyouzi
	</div>
	<hr size=1>
	<table width="70%" border="0" cellspacing="0" cellpadding="5" align=center>
	<tr><td colspan=3>
	●最近の試合
	</td></tr>
	<tr  class=jouge bgcolor=#ffff66 align=center><td>対　戦</td><td nowrap>勝　者</td><td nowrap>決めのコメント</td></tr>
EOM

	$i=1;
#	foreach (@alldata) {
	foreach (@aite_erabi) { #koko2005/08/03
		($ch_k_id,$ch_name,$ch_oyaname,$ch_gazou,$ch_kati,$ch_make,$ch_hikiwake,$ch_yuusyou,$ch_lasttime,$ch_yobi1,$ch_yobi2,$ch_yobi3,$ch_yobi4,$ch_yobi5,$ch_yobi6)= split(/<>/);
		print "<tr class=sita2>$ch_yobi1</tr>";
				if($i >=5){last;}
			$i++;
	}

	print <<"EOM";
	</table><br><br>
	<table width="70%" border="0" cellspacing="0" cellpadding="5" align=center>
	<tr><td colspan=7>
	●現在までの順位（ベスト10）
	</td></tr>
	<tr  class=jouge bgcolor=#ffff66 align=center><td></td><td nowrap>名前</td><td>作成者</td><td>勝　利</td><td nowrap>敗　戦</td><td>引き分け</td><td>試合消化数</td><td nowrap>優勝回数</td></tr>
EOM

	$i=1;
	foreach (@junidata) {
		($ch_k_id,$ch_name,$ch_oyaname,$ch_gazou,$ch_kati,$ch_make,$ch_hikiwake,$ch_yuusyou,$ch_lasttime,$ch_yobi1,$ch_yobi2,$ch_yobi3,$ch_yobi4,$ch_yobi5,$ch_yobi6)= split(/<>/);
		if ($i <= 3 && $ch_gazou ne ""){$ch_name_hyouzi = "<img src=$ch_gazou $chara_gazou_size><br>$ch_name";}else{$ch_name_hyouzi = "$ch_name";}
		$siaisyouka = $ch_kati + $ch_make + $ch_hikiwake;
		print <<"EOM";
		<tr class=sita2><td align=center>$i</td><td nowrap align=center>$ch_name_hyouzi</td><td align=center>$ch_oyaname</td><td align=right nowrap>$ch_kati勝</td><td align=right nowrap>$ch_make敗</td><td align=right>$ch_hikiwake分け</td><td align=right nowrap>$siaisyouka</td><td align=right nowrap>$ch_yuusyou回</td></tr>
EOM
				if($i >=10){last;}
			$i++;
	}
	print "</table>";
	
	if ($nankai_taikai != 1){ 
	print <<"EOM";
	<br><br>
	<table width="70%" border="0" cellspacing="0" cellpadding="5" align=center>
	<tr><td colspan=7>
	●前回大会の順位（ベスト5）
	</td></tr>
	<tr  class=jouge bgcolor=#ffff66 align=center><td></td><td nowrap>名前</td><td>作成者</td><td>勝　利</td><td nowrap>敗　戦</td><td>引き分け</td><td nowrap>優勝回数</td></tr>
EOM

	$i=1;
	foreach (@zenkaijunidata) {
		($ch_k_id,$ch_name,$ch_oyaname,$ch_gazou,$ch_kati,$ch_make,$ch_hikiwake,$ch_yuusyou,$ch_lasttime,$ch_yobi1,$ch_yobi2,$ch_yobi3,$ch_yobi4,$ch_yobi5,$ch_yobi6)= split(/<>/);
		if ($i == 1 && $ch_gazou ne ""){$ch_name_hyouzi = "<img src=$ch_gazou $chara_gazou_size><br>$ch_name";}else{$ch_name_hyouzi = "$ch_name";}
		$siaisyouka = $ch_kati + $ch_make + $ch_hikiwake;
		print <<"EOM";
		<tr class=sita2><td align=center>$i</td><td nowrap align=center>$ch_name_hyouzi</td><td align=center>$ch_oyaname</td><td align=right nowrap>$ch_yobi3勝</td><td align=right nowrap>$ch_yobi4敗</td><td align=right>$ch_yobi5分け</td><td align=right nowrap>$ch_yuusyou回</td></tr>
EOM
				if($i >= 5){last;}
			$i++;
	}
	print "</table>";
	print <<"EOM";
	<br><br>
	<table width="70%" border="0" cellspacing="0" cellpadding="5" align=center>
	<tr><td colspan=7>
	●総合順位（ポイント獲得ベスト10）<br>
	優勝＝10ポイント、２位＝5ポイント、３位＝3ポイント、４位＝2ポイント、５位＝1ポイントが加算され、その累積ポイント数で決定します。
	</td></tr>
	<tr  class=jouge bgcolor=#ffff66 align=center><td></td><td nowrap>名前</td><td>作成者</td><td>獲得ポイント</td><td nowrap>優勝回数</td></tr>
EOM

	$i=1;
	foreach (@sougoujunidata) {
		($ch_k_id,$ch_name,$ch_oyaname,$ch_gazou,$ch_kati,$ch_make,$ch_hikiwake,$ch_yuusyou,$ch_lasttime,$ch_yobi1,$ch_yobi2,$ch_yobi3,$ch_yobi4,$ch_yobi5,$ch_yobi6)= split(/<>/);
		if ($ch_yobi2 eq ""){next;}
		if ($i <= 3 && $ch_gazou ne ""){$ch_name_hyouzi = "<img src=$ch_gazou $chara_gazou_size><br>$ch_name";}else{$ch_name_hyouzi = "$ch_name";}
		$siaisyouka = $ch_kati + $ch_make + $ch_hikiwake;
		print <<"EOM";
		<tr class=sita2><td align=center>$i</td><td nowrap align=center>$ch_name_hyouzi</td><td align=center>$ch_oyaname</td><td align=right nowrap>$ch_yobi2ポイント</td><td align=right nowrap>$ch_yuusyou回</td></tr>
EOM
				if($i >= 10){last;}
			$i++;
	}
	print "</table>";
	
	}		#１回大会でない場合の閉じ
		&hooter("login_view","戻る");
		exit;
}

#####Cリーグへの登録処理
sub c_league_touroku {
	open(TO,"< $doukyo_logfile") || &error("Open Error : $doukyo_logfile");
	eval{ flock (TO, 2); };
	my @touroku_list = <TO>;
	close(TO);	
	my($ch2_k_id,$ch2_name,$ch2_oyaname,$ch2_gazou)= split(/<>/,@_[0]);
	$c_sinki_temp = "$ch2_k_id<>$ch2_name<>$ch2_oyaname<>$ch2_gazou<>0<>0<>0<>0<>$ch2_lasttime<>$ch2_yobi1<>$ch2_yobi2<>$ch2_yobi3<>$ch2_yobi4<>$ch2_yobi5<>$ch2_yobi6<>\n"; 
	push (@touroku_list,$c_sinki_temp);
	open(TOO,">$doukyo_logfile") || &error("Open Error : $doukyo_logfile");
	eval{ flock (TOO, 2); };
	print TOO @touroku_list;
	close(TOO);
	$my_genzaino_joukyou = "$c_sinki_temp";		#自分の状況を変数に入れておく
}

sub ch_kougeki {
#攻撃内容をランダムで選択
		$battle_rand = int(rand(17))+1;
		print "<table width=\"600\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\" align=center><tr align=center><td>";
##自分の攻撃の場合
		if (@_[0] == 1){
			print "<div style=\"color:#339933;font-size:12px;\" align=left>@_[1]の攻撃！<br>";
#攻撃内容
			&ch_kougekinaiyou (1,$aite_chara_para[1]);
#結果表示
			if ($damage eq "no_d"){
					print "<div style=\"color:#ff3300;font-size:12px;\" align=right>$return_naiyou</div>\n";
			}else{
					print "<div style=\"color:#339933;font-size:12px;\" align=right>$return_naiyou</div>\n";
					$aite_chara_power -= $damage;
			}
			
##相手の攻撃の場合
		}else {
			print "<div style=\"color:#ff3300;font-size:12px;\" align=right>@_[1]の攻撃！<br>";
			&ch_kougekinaiyou (0,$my_chara_para[1]);
#結果表示
#自分にきかない場合
			if ($damage eq "no_d"){
					print "<div style=\"color:#339933;font-size:12px;\" align=left>$return_naiyou</div>\n";
			}else{
#ダメージを受けた場合
					print "<div style=\"color:#ff3300;font-size:12px;\" align=left>$return_naiyou</div>\n";
					$my_chara_power -= $damage;
			}
		}
	print "</td></tr></table>";
}

###攻撃内容ごとのダメージ処理サブルーチン
sub ch_kougekinaiyou {
# @_[0]＝1なら自分の攻撃、0なら相手の攻撃
	if (@_[0] == 1){$align_settei = "align=left";}else{$align_settei = "align=right";}
	
			$battle_naiyou_hanbetu = $battle_rand + 26;	#バトルランダム値の１が国語のコメントになるようにする
			if ($battle_rand <= 8 || $battle_rand == 15 || $battle_rand == 16){
				$seisinornikutai = "精神的ダメージを受けた！";
			}else{$seisinornikutai = "肉体的ダメージを受けた！";}
			if (@_[0] == 1){
				print "$my_chara_para[$battle_naiyou_hanbetu]</div><br>\n";
			}else{
				print "$aite_chara_para[$battle_naiyou_hanbetu]</div><br>\n";
			}
# iryoku_hantei (攻撃者,攻撃の内容)
			&ch_iryoku_hantei (@_[0],$battle_rand);
			if ($damage eq "no_d"){$return_naiyou = "@_[1]はダメージを受けなかった。";}
			else{$return_naiyou = "@_[1]は <span style=\"font-size:18px\">$damage</span> の$seisinornikutai";}

	if (@_[0] == 1 && $damage ne "no_d"){$dameegitame += $damage;}	#koko 2005/04/17

}

#威力判定サブルーチン
sub ch_iryoku_hantei {
#攻撃の内容ごとの能力値
	$iryoku_hanteiti = @_[1] + 5;		#バトルランダム値の１が国語の能力になるようにする
#koko2007/10/13
	$myrad1 = int(rand(3));
	if($myrad1 == 0){
		$batoru1 = $my_chara_para[$iryoku_hanteiti] - int($my_chara_para[$iryoku_hanteiti] / 3);
	}elsif($myrad1 == 1){
		$batoru1 = $my_chara_para[$iryoku_hanteiti] + int($my_chara_para[$iryoku_hanteiti] / 3);
	}else{
		$batoru1 = $my_chara_para[$iryoku_hanteiti];
	}
	$myrad2 = int(rand(3));
	if($myrad2 == 0){
		$batoru2 = $aite_chara_para[$iryoku_hanteiti] - int($aite_chara_para[$iryoku_hanteiti] / 3);
	}elsif($myrad2 == 1){
		$batoru2 = $aite_chara_para[$iryoku_hanteiti] + int($aite_chara_para[$iryoku_hanteiti] / 3);
	}else{
		$batoru2 = $aite_chara_para[$iryoku_hanteiti];
	}
	if (@_[0] == 1){
		$hantei_kakkati = $batoru1 - $batoru2;
	}else{
		$hantei_kakkati = $batoru2 - $batoru1;
	}
#end2007/10/13
	if ($hantei_kakkati <= 0){
			$damage = "no_d";
	}else{
			$damage = "$hantei_kakkati";
	}
}

###大会初期化処理
sub taikai_syokika {
			&lock;
	@alldata = (); #koko2007/07/16
	foreach (@aite_erabi){
		my ($ch_k_id,$ch_name,$ch_oyaname,$ch_gazou,$ch_kati,$ch_make,$ch_hikiwake,$ch_yuusyou,$ch_lasttime,$ch_yobi1,$ch_yobi2,$ch_yobi3,$ch_yobi4,$ch_yobi5,$ch_yobi6)= split(/<>/);
#koko2005/08/03			$key=(split(/<>/,$_))[4];		#ソートする要素を選ぶ
			push @alldata,$_;
#			push @keys,$key;
	}
	
#		sub bykeys{$keys[$b] <=> $keys[$a];}
#		@junidata=@alldata[ sort bykeys 0..$#alldata]; 
		@keys0 = map {(split /<>/)[4]} @alldata;
		@junidata = @alldata[sort {$keys0[$b] <=> $keys0[$a]} 0 .. $#keys0];
#kokoend

	$i = 1;
	@new_aite_erabi = (); #koko2007/07/16
	foreach (@junidata){
		($ch_k_id,$ch_name,$ch_oyaname,$ch_gazou,$ch_kati,$ch_make,$ch_hikiwake,$ch_yuusyou,$ch_lasttime,$ch_yobi1,$ch_yobi2,$ch_yobi3,$ch_yobi4,$ch_yobi5,$ch_yobi6)= split(/<>/);
		$ch_yobi3 = $ch_kati;
		$ch_yobi4 = $ch_make;
		$ch_yobi5 = $ch_hikiwake;
		$ch_kati = 0;
		$ch_make = 0;
		$ch_hikiwake = 0;
		if ($i == 1){$ch_yuusyou ++; $ch_yobi2 += 10;}
		if ($i == 2){$ch_yobi2 += 5;}
		if ($i == 3){$ch_yobi2 += 3;}
		if ($i == 4){$ch_yobi2 += 2;}
		if ($i == 5){$ch_yobi2 += 1;}
		$c_sinki_temp = "$ch_k_id<>$ch_name<>$ch_oyaname<>$ch_gazou<>$ch_kati<>$ch_make<>$ch_hikiwake<>$ch_yuusyou<>$ch_lasttime<>$ch_yobi1<>$ch_yobi2<>$ch_yobi3<>$ch_yobi4<>$ch_yobi5<>$ch_yobi6<>\n"; 
		push (@new_aite_erabi,$c_sinki_temp);
		$i ++;
	}
			$nankai_taikai ++;
			$league_meisai = "$now_time<>$nankai_taikai<>\n";
			@aite_erabi = @new_aite_erabi;
			@alldata = ();
			$nannitime = 1;
			unshift (@new_aite_erabi,$league_meisai);
			open(OUT,">$doukyo_logfile") || &error("Open Error : $doukyo_logfile");
			eval{ flock (OUT, 2); };
			print OUT @new_aite_erabi;
			close(OUT);			
			&unlock;
	
}

#######新規登録処理
sub new_hyouji {
	if ($tajuukinsi_flag==1){$tajuucomment = "<br>※多重登録は禁止です。";}
	if ($tajuukinsi_deny==1){$tajuucomment .= "<br>多重登録が発覚した時点でログインできなくなりますのでご注意ください。";}

	&header(syokudou_style);
	print <<"EOM";
	<script type="text/javascript" language="JavaScript"><!-- 
		function keisan(kazu){
			if(kazu == 1){
				kokugo = eval(document.myForm.kokugo.value);
				suugaku = eval(document.myForm.suugaku.value);
				rika = eval(document.myForm.rika.value);
				syakai = eval(document.myForm.syakai.value);
				eigo = eval(document.myForm.eigo.value);
				ongaku = eval(document.myForm.ongaku.value);
				bijutu = eval(document.myForm.bijutu.value);
				
                all_para = kokugo + suugaku + rika + syakai + eigo + ongaku + bijutu;
                
                if(isNaN(all_para)){
                	all_para = all_para + "　<font color=red><b>※数値を入力してください。</b></font>";
                }else if(all_para > 200){
                	all_para = all_para + "　<font color=red><b>※上限値２００を超えています。</b></font>";
                }
                
                if (document.all){
                	document.all("goukei1").innerHTML = all_para;
                }else if(document.getElementById){
					document.getElementById("goukei1").innerHTML = all_para;
				}
			}else if(kazu == 2){
				looks = eval(document.myForm.looks.value);
				tairyoku = eval(document.myForm.tairyoku.value);
				kenkou = eval(document.myForm.kenkou.value);
				speed = eval(document.myForm.speed.value);
				power = eval(document.myForm.power.value);
				wanryoku = eval(document.myForm.wanryoku.value);
				kyakuryoku = eval(document.myForm.kyakuryoku.value);
				
                all_para = looks + tairyoku + kenkou + speed + power + wanryoku + kyakuryoku;
                
                if(isNaN(all_para)){
                	all_para = all_para + "　<font color=red><b>※数値を入力してください。</b></font>";
                }else if(all_para > 200){
                	all_para = all_para + "　<font color=red><b>※上限値２００を超えています。</b></font>";
                }
                
                if (document.all){
                	document.all("goukei2").innerHTML = all_para;
                }else if(document.getElementById){
					document.getElementById("goukei2").innerHTML = all_para;
				}
			}else if(kazu == 3){
				love = eval(document.myForm.love.value);
				unique = eval(document.myForm.unique.value);
				etti = eval(document.myForm.etti.value);
				
                all_para = love + unique + etti;
                
                if(isNaN(all_para)){
                	all_para = all_para + "　<font color=red><b>※数値を入力してください。</b></font>";
                }else if(all_para > 100){
                	all_para = all_para + "　<font color=red><b>※上限値１００を超えています。</b></font>";
                }
                
                if (document.all){
                	document.all("goukei3").innerHTML = all_para;
                }else if(document.getElementById){
					document.getElementById("goukei3").innerHTML = all_para;
				}
			}
		}
		
		function setrand(kazu){
			if(kazu == 1){
			    nouryoku = new Array(0, 0, 0, 0, 0, 0, 0);
				for (i = 0; i < 10; i++) {
					rand = Math.floor( Math.random() * 7 );
					nouryoku[rand]++;
				}
				document.myForm.kokugo.value = 30 - nouryoku[0];
				document.myForm.suugaku.value = 30 - nouryoku[1];
				document.myForm.rika.value = 30 - nouryoku[2];
				document.myForm.syakai.value = 30 - nouryoku[3];
				document.myForm.eigo.value = 30 - nouryoku[4];
				document.myForm.ongaku.value = 30 - nouryoku[5];
				document.myForm.bijutu.value = 30 - nouryoku[6];
				keisan(1);
			}else if(kazu == 2){
			    nouryoku = new Array(0, 0, 0, 0, 0, 0, 0);
				for (i = 0; i < 10; i++) {
					rand = Math.floor( Math.random() * 7 );
					nouryoku[rand]++;
				}
				document.myForm.looks.value = 30 - nouryoku[0];
				document.myForm.tairyoku.value = 30 - nouryoku[1];
				document.myForm.kenkou.value = 30 - nouryoku[2];
				document.myForm.speed.value = 30 - nouryoku[3];
				document.myForm.power.value = 30 - nouryoku[4];
				document.myForm.wanryoku.value = 30 - nouryoku[5];
				document.myForm.kyakuryoku.value = 30 - nouryoku[6];
				keisan(2);
			}else if(kazu == 3){
			    nouryoku = new Array(0, 0, 0);
				for (i = 0; i < 10; i++) {
					rand = Math.floor( Math.random() * 3 );
					nouryoku[rand]++;
				}
				document.myForm.love.value = 30 + nouryoku[0];
				document.myForm.unique.value = 30 + nouryoku[1];
				document.myForm.etti.value = 30 + nouryoku[2];
				keisan(3);
			}		
		}
	  --></script>

	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>ここであなたのキャラクターを登録することができます。<br>名前（本名よりＨＮのほうが○）とパスワードと性別を決めて入力してください。<br>また、最初の能\力値は指定値以下になるように振り分けてください。<br>紹介コードがある場合も入力してください。<br>誰にも紹介されてなく、紹介コードがない場合には「no」と入力してください。<br><font color="red">$tajuucomment</font></td>
	<td bgcolor="#333333" align="center" width="35%" valign="middle"><h1><font color="#ffffff">新規登録場</font></h1></td>
	</tr></table><br>

	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
		<form method="POST" action="game.cgi" name="myForm">
		<input type=hidden name=mode value="new">
		<tr>
			<td bgcolor="#eeeeee">
            	<b>名前</b>（変更はできないので慎重に決めてください。）
			</td>
		</tr>
		<tr>
			<td>
				<input type="text" name="name" size="50" onmouseover="this.focus()" onfocus="this.select()" maxlength="20">
			</td>
		</tr>
		<tr>
			<td bgcolor="#eeeeee">
            	<b>パスワード</b>（人に分かりにくく、自分で覚えやすいものにしてください。）
			</td>
		</tr>
		<tr>
			<td>
				<input type="text" name="pass" size="50" onmouseover="this.focus()" onfocus="this.select()" maxlength="20">
			</td>
		</tr>
		<tr>
			<td bgcolor="#eeeeee">
            	<b>紹介コード</b>（ない、意味が分からない場合には「no」と入力してください。）
			</td>
		</tr>
		<tr>
			<td>
				<input type="text" name="syokai" size="50" onmouseover="this.focus()" onfocus="this.select()" maxlength="20" value="no">
			</td>
		</tr>
		<tr>
			<td bgcolor="#eeeeee">
            	<b>性別</b>（結婚や仕事や最初の身長、体重に関係します。）
			</td>
		</tr>
		<tr>
			<td>
				<input type="radio" name="sex" value="m" checked>男
				<input type="radio" name="sex" value="f">女
			</td>
		</tr>
		<tr>
			<td bgcolor="#eeeeee">
            	<b>頭　脳の能\力値</b>　<span style="color:blue;text-decoration:underline;cursor:pointer;" onclick="setrand(1)">ランダム設定</span>　現在の合計値：<span id="goukei1">0</span>（最大２００）
			</td>
		</tr>
		<tr>
			<td>
				国語：<input type="text" name="kokugo" size="3" onkeyup="keisan(1)" value="0">
				数学：<input type="text" name="suugaku" size="3" onkeyup="keisan(1)" value="0">
				理科：<input type="text" name="rika" size="3" onkeyup="keisan(1)" value="0">
				社会：<input type="text" name="syakai" size="3" onkeyup="keisan(1)" value="0">
				英語：<input type="text" name="eigo" size="3" onkeyup="keisan(1)" value="0">
				音楽：<input type="text" name="ongaku" size="3" onkeyup="keisan(1)" value="0">
				美術：<input type="text" name="bijutu" size="3" onkeyup="keisan(1)" value="0">
			</td>
		</tr>
		<tr>
			<td bgcolor="#eeeeee">
            	<b>身　体の能\力値</b>　<span style="color:blue;text-decoration:underline;cursor:pointer;" onclick="setrand(2)">ランダム設定</span>　現在の合計値：<span id="goukei2">0</span>
			</td>
		</tr>
		<tr>
			<td>
				ルックス：<input type="text" name="looks" size="3" onkeyup="keisan(2)" value="0">
				体力：<input type="text" name="tairyoku" size="3" onkeyup="keisan(2)" value="0">
				健康：<input type="text" name="kenkou" size="3" onkeyup="keisan(2)" value="0">
				スピード：<input type="text" name="speed" size="3" onkeyup="keisan(2)" value="0">
				パワー：<input type="text" name="power" size="3" onkeyup="keisan(2)" value="0">
				腕力：<input type="text" name="wanryoku" size="3" onkeyup="keisan(2)" value="0">
				脚力：<input type="text" name="kyakuryoku" size="3" onkeyup="keisan(2)" value="0">
			</td>
		</tr>
		<tr>
			<td bgcolor="#eeeeee">
            	<b>その他の能\力値</b>　<span style="color:blue;text-decoration:underline;cursor:pointer;" onclick="setrand(3)">ランダム設定</span>　現在の合計値：<span id="goukei3">0</span>（最大１００）
			</td>
		</tr>
		<tr>
			<td>
				LOVE：<input type="text" name="love" size="3" onkeyup="keisan(3)" value="0">
				面白さ：<input type="text" name="unique" size="3" onkeyup="keisan(3)" value="0">
				エッチ：<input type="text" name="etti" size="3" onkeyup="keisan(3)" value="0">
			</td>
		</tr>
		<tr>
			<td colspan="2" align="center">
				<input type="submit" value="登録する">
			</td>
		</tr>
		</form>
	</table>
	<div align="center"><a href=\"javascript:history.back()\"> [前の画面に戻る] </a></div>
EOM
	exit;
}

#######新規登録処理
sub new {
	if ($new_touroku_per == 1) {&error("現在、新規登録を中止しています。");}
	&lock;
	&get_host;
	if($in{'name'} eq '' || $in{'pass'} eq '' || $in{'sex'} eq ''){&error("記入漏れがあります！");}
	if($in{'name'}  =~ / / || $in{'name'}  =~ /　/){&error("名前にスペースを使わないでください");}
	if($in{'name'}  =~ /,/){&error("名前に「,」を使わないでください");}
    
	open(IN,"< $logfile") || &error("Open Error : $logfile");
	eval{ flock (IN, 2); };
	@all_sankasya = <IN>;

	foreach (@tazyu_kyoka){if ($in{'name'} eq $_){$kyoka_ok = 1;}}
	
	foreach (@all_sankasya) {
		&kozin_sprit;
		if($in{'name'} eq $name){ &error("その名前はすでに登録されています。別の名前でお試しください。");}
		if ($tajuukinsi_flag==1){
			if($return_host eq $host && !$kyoka_ok){ &error("二重登録は禁止です。");}
		}
	}
	close(IN);
    
	#ランダム紹介判定
	if($in{'syokai'} eq $in_aikotoba && $in_aikotoba ne ''){
		$my_m_comment = "$in{'name'}さんが新規登録され、新しいメンバーになりました。";
	}elsif ($syokai eq 'yes' ){
		($in_syoukai_id,$no) = split(/=/, $in{'syokai'});
		if (!$in_syoukai_id){ &error("紹介コードがありません。");}
		if (!$no){&error("紹介してくれた相手がいません。");}
		
		#紹介者のファイルがあったらファイルをオープン
		$aite_f = "./member/$no/log.cgi";
		if (! -e $aite_f){&error("紹介者が見つかりません。");}
		open (IN,"< $aite_f" || &error("ファイルを開くことが出来ませんでした。"));
		eval{ flock (IN, 2); };
		$aite_tep = <IN>;
		close(IN);
		&aite_sprit($aite_tep);
		if ($aite_syoukai_id ne $in_syoukai_id){&error("知り合いからコードを聞いて登録してください。");}
		
		#紹介者に紹介料の振り込み。
		if ($syoukai_majin eq 'yes'){
			$okane = 1000000;
            
			&openAitelog ($no);
			$aite_kpoint += 50;
			$aite_bank += $okane;
			&aite_temp_routin;
			open(OUT,">$aite_log_file") || &error("$aite_log_fileが開けません");
			eval{ flock (OUT, 2); };
			print OUT $aite_k_temp;
			close(OUT);
			&aite_kityou_syori("紹介料($in{'name'})","",$okane,$aite_bank,"普",$no,"lock_off");
		}
        
		$syoukai_ari = 1;
		$my_m_comment = "$in{'name'}さんが新規登録され、新しいメンバーになりました。$in{'syokai'} $aite_nameからの紹介です。";
		$aite_syoukai_id = "";
		
		#紹介者のファイルがあったらファイルをオープン紹介相手のファイルを書き直し。
		open(OUT,">$aite_f") || &error("$aite_fに書き込めません");
		eval{ flock (OUT, 2); };
		&aite_temp_routin;
		print OUT $aite_k_temp;
		close(OUT);
	}elsif($in{'syokai'} ne $in_aikotoba && $syokai eq ''){
		&error("知り合いからコードを聞いて登録してください。");
	}else{
		$my_m_comment = "$in{'name'}さんが新規登録され、新しいメンバーになりました。";
	}

	#パスワードリストから新規IDを取得
	open(PA,"< $pass_logfile") || &error("Open Error : $pass_logfile");
	eval{ flock (PA, 2); };
	@all_pass_list = <PA>;
	close(PA);
	($saisin_id)= split(/<>/,$all_pass_list[0]);
	$saisin_id ++;
	
	#ステータスが正しいか確認
	if($in{'kokugo'} =~ /[^0-9]/){&error("数値が不適切です");}
	if($in{'suugaku'} =~ /[^0-9]/){&error("数値が不適切です");}
	if($in{'rika'} =~ /[^0-9]/){&error("数値が不適切です");}
	if($in{'syakai'} =~ /[^0-9]/){&error("数値が不適切です");}
	if($in{'eigo'} =~ /[^0-9]/){&error("数値が不適切です");}
	if($in{'ongaku'} =~ /[^0-9]/){&error("数値が不適切です");}
	if($in{'bijutu'} =~ /[^0-9]/){&error("数値が不適切です");}
	if($in{'looks'} =~ /[^0-9]/){&error("数値が不適切です");}
	if($in{'tairyoku'} =~ /[^0-9]/){&error("数値が不適切です");}
	if($in{'kenkou'} =~ /[^0-9]/){&error("数値が不適切です");}
	if($in{'speed'} =~ /[^0-9]/){&error("数値が不適切です");}
	if($in{'power'} =~ /[^0-9]/){&error("数値が不適切です");}
	if($in{'wanryoku'} =~ /[^0-9]/){&error("数値が不適切です");}
	if($in{'kyakuryoku'} =~ /[^0-9]/){&error("数値が不適切です");}
	if($in{'love'} =~ /[^0-9]/){&error("数値が不適切です");}
	if($in{'unique'} =~ /[^0-9]/){&error("数値が不適切です");}
	if($in{'etti'} =~ /[^0-9]/){&error("数値が不適切です");}
	
	if($in{'kokugo'} <= 0){&error("０またはそれ以下の能\力があります。");}
	if($in{'suugaku'} <= 0){&error("０またはそれ以下の能\力があります。");}
	if($in{'rika'} <= 0){&error("０またはそれ以下の能\力があります。");}
	if($in{'syakai'} <= 0){&error("０またはそれ以下の能\力があります。");}
	if($in{'eigo'} <= 0){&error("０またはそれ以下の能\力があります。");}
	if($in{'ongaku'} <= 0){&error("０またはそれ以下の能\力があります。");}
	if($in{'bijutu'} <= 0){&error("０またはそれ以下の能\力があります。");}
	if($in{'looks'} <= 0){&error("０またはそれ以下の能\力があります。");}
	if($in{'tairyoku'} <= 0){&error("０またはそれ以下の能\力があります。");}
	if($in{'kenkou'} <= 0){&error("０またはそれ以下の能\力があります。");}
	if($in{'speed'} <= 0){&error("０またはそれ以下の能\力があります。");}
	if($in{'power'} <= 0){&error("０またはそれ以下の能\力があります。");}
	if($in{'wanryoku'} <= 0){&error("０またはそれ以下の能\力があります。");}
	if($in{'kyakuryoku'} <= 0){&error("０またはそれ以下の能\力があります。");}
	if($in{'love'} <= 0){&error("０またはそれ以下の能\力があります。");}
	if($in{'unique'} <= 0){&error("０またはそれ以下の能\力があります。");}
	if($in{'etti'} <= 0){&error("０またはそれ以下の能\力があります。");}
	
	if($in{'kokugo'} + $in{'suugaku'} + $in{'rika'} + $in{'syakai'} + $in{'eigo'} + $in{'ongaku'} + $in{'bijutu'} > 200){&error("上限値２００を超えています。");}
	if($in{'looks'} + $in{'tairyoku'} + $in{'kenkou'} + $in{'speed'} + $in{'power'} + $in{'wanryoku'} + $in{'kyakuryoku'} > 200){&error("上限値２００を超えています。");}
	if($in{'love'} + $in{'unique'} + $in{'etti'} > 100){&error("上限値１００を超えています。");}
	
	if($in{'sex'} eq "m"){
			$sintyou= 165 + (int(rand(20)));
	}else{
			$sintyou= 150 + (int(rand(25)));
	}
	if($in{'sex'} eq "m"){
			$taijuu= 50 + (int(rand(35)));
	}else{
			$taijuu= 48 + (int(rand(20)));
	}
	&time_get;
	$last_syokuzi = $date_sec - ($syokuzi_kankaku*60);
	if($syoukai_ari){$syoukai_in = 1000000;}else{$syoukai_in = 100000;}
	if($syoukai_ari){$kpoint = 50;}else{$kpoint = 0;}
	
	$new_temp="$saisin_id<>$in{'name'}<>$in{'pass'}<>$syoukai_in<>0<>日払いバイト<>$in{'kokugo'}<>$in{'suugaku'}<>$in{'rika'}<>$in{'syakai'}<>$in{'eigo'}<>$in{'ongaku'}<>$in{'bijutu'}<>$in{'looks'}<>$in{'tairyoku'}<>$in{'kenkou'}<>$in{'speed'}<>$in{'power'}<>$in{'wanryoku'}<>$in{'kyakuryoku'}<>$in{'love'}<>$in{'unique'}<>$in{'etti'}<>$date_sec<><>$in{'sex'}<>$date_sec<>$date<>$return_host<><><><><><>0<>100<><><>$last_syokuzi<>$sintyou<>$taijuu<>100<><>0<>0<><>50<><><><><>$k_yobi3<><>0<><><>\n";
	
	$pass_temp = "$saisin_id<>$in{'name'}<>$in{'pass'}<>\n";
	
	#自分用ディレクトリ＆ログファイル作成
	$my_directry = "./member/$saisin_id";
	$my_log_file = "$my_directry/log.cgi";
	mkdir($my_directry, 0755) || &error("ID番号$saisin_idのディレクトリが既に存在しています。");
	if ($zidouseisei == 1){
		chmod 0777,"$my_directry";
	}elsif ($zidouseisei == 2){
		chmod 0755,"$my_directry";
	}else{
		chmod 0755,"$my_directry";
	}
	open(MYF,">$my_log_file") || &error("Open Error : $my_log_file");
	eval{ flock (MYF, 2); };
	print MYF $new_temp;
	chmod 0666,"$my_log_file";
	close(MYF);
	
	#メッセージ交換用ファイル作成
	$message_file="$my_directry/mail.cgi";
	open(MF,">$message_file") || &error("Write Error : $message_file");
	eval{ flock (MF, 2); };
	chmod 0666,"$message_file";
	close(MF);
    
	#送り先が無い時の処理
	if($kanrisyaname ne ''){
		open(AIT,"< $message_file") || &error("お相手の方のメール記録ファイル（$message_file）が開けません。");
		eval{ flock (AIT, 1); };
		$last_mail_check_time = <AIT>;
		@mail_cont = <AIT>;
		close(AIT);

		&time_get;
		$new_mail = "受信<>$kanrisyaname<>$m_comment<>$date2<>$date_sec<><><><><><>\n";
		unshift (@mail_cont,$new_mail);
		if (@mail_cont > $mail_hozon_gandosuu){pop @mail_cont;}
		
		#最終メールチェック時間がなければ１を入れる
		if ($last_mail_check_time eq ""){$last_mail_check_time = "1\n";}
		unshift (@mail_cont,$last_mail_check_time);
        
		open(OUT,">$message_file") || &error("$message_fileに書き込めません");
		eval{ flock (OUT, 2); };
		print OUT @mail_cont;
		close(OUT);

		#自分のメールにも送信済みメッセージとして記録（管理者メールでなければ）
		$my_sousin_file="./member/$kanrisya_id/mail.cgi";
		if (-e "$my_sousin_file"){#管理者がない時送信無し。
			open(ZIB,"< $my_sousin_file") || &error("$my_sousin_fileが開けません。");
			eval{ flock (ZIB, 1); };
			$my_last_mail_check_time = <ZIB>;
			@my_mail_cont = <ZIB>;
			close(ZIB);
			
			$sousin_mail = "受信<>$in{'name'}<>$my_m_comment<>$date2<>$date_sec<><><><><><>\n";
			unshift (@my_mail_cont,$sousin_mail);
			if (@my_mail_cont > $mail_hozon_gandosuu){pop @my_mail_cont;}
			
			#最終メールチェック時間がなければ今の時間を入れる
			if ($my_last_mail_check_time eq ""){$my_last_mail_check_time = "$date_sec\n";}
			unshift (@my_mail_cont,$my_last_mail_check_time);
            
			open(ZIBO,">$my_sousin_file") || &error("$my_sousin_fileに書き込めません");
			eval{ flock (ZIBO, 2); };
			print ZIBO @my_mail_cont;
			close(ZIBO);
		}
	}

	#購入物記録ファイル作成
	$monokiroku_file="$my_directry/mono.cgi";
	open(MK,">$monokiroku_file") || &error("Write Error : $monokiroku_file");
	eval{ flock (MK, 2); };
	chmod 0666,"$monokiroku_file";
	close(MK);
	
	#銀行明細記録ファイル作成
	$ginkoumeisai_file="$my_directry/ginkoumeisai.cgi";
	open(GM,">$ginkoumeisai_file") || &error("Write Error : $ginkoumeisai_file");
	eval{ flock (GM, 2); };
	chmod 0666,"$ginkoumeisai_file";
	close(GM);

	#リスト用ログファイル作成
	push (@all_sankasya,$new_temp);
	if ($mem_lock_num == 0){
		$err = &data_save($logfile, @all_sankasya);
		if ($err) {&error("$err");}
	}else{
		open(OUT,">>$logfile") || &error("Write Error : $logfile");
		eval{ flock (OUT, 2); };
		print OUT $new_temp;
		close(OUT);
	}
	
	#パスワード記録ファイル更新
	unshift (@all_pass_list,$pass_temp);
		open(PAO,">$pass_logfile") || &error("Write Error : $pass_logfile");
		eval{ flock (PAO, 2); };
		print PAO @all_pass_list;
		close(PAO);

	#ニュース記録
	&news_kiroku("入居","$in{'name'}さんが新しい住民になりました。");		#ver.1.3

	&unlock;
	&set_cookie;
	
	#表示
	&header;
	&check_pass;
	print <<"EOM";
	<div align=center>
	<br><br>以下の内容で住民登録が完了しました。<br><br>
<font color="red"><a href="./kiyaku.html"><img border="0" src="img/kiyaku.gif"></a>←ここを読んでください！</font>	
<table width="450" border="0" cellspacing="0" cellpadding="4" align=center style=" border: $st_win_wak; border-style: solid; border-top-width: 1px; border-right-width: 1px; border-bottom-width: 1px; border-left-width: 1px" bgcolor=$st_win_back>
<tr>
<td  width="25%"><span class=honbun2>名前</span>：$name</td>
<td><span class=honbun2>パス</span>：$pass</td>
<td width="25%"><span class=honbun2>身長</span>：$sintyou</td>
<td width="25%"><span class=honbun2>体重</span>：$taijuu</td></tr>
<tr style=" border: $st_win_wak; border-style: solid; border-top-width: 1px; border-right-width: 0px; border-bottom-width: 0px; border-left-width: 0px">
<td  width="25%"><span class=tyuu>◆頭脳</span></td>
<td><span class=honbun2>国語</span>：$kokugo</td>
<td width="25%"><span class=honbun2>数学</span>：$suugaku</td>
<td width="25%"><span class=honbun2>理科</span>：$rika</td></tr>
<tr><td width="25%"><span class=honbun2>社会</span>：$syakai</td>
<td width="25%"><span class=honbun2>英語</span>：$eigo</td>
<td width="25%"><span class=honbun2>音楽</span>：$ongaku</td>
<td width="25%"><span class=honbun2>美術</span>：$bijutu</td></tr>
<tr style=" border: $st_win_wak; border-style: solid; border-top-width: 1px; border-right-width: 0px; border-bottom-width: 0px; border-left-width: 0px"><td  width="25%"><span class=tyuu>◆身体</span></td>
<td><span class=honbun2>ルックス</span>：$looks</td>
<td><span class=honbun2>体力</span>：$tairyoku</td>
<td><span class=honbun2>健康</span>：$kenkou</td></tr>
<tr><td><span class=honbun2>スピード</span>：$speed</td>
<td><span class=honbun2>パワー</span>：$power</td>
<td><span class=honbun2>腕力</span>：$wanryoku</td>
<td><span class=honbun2>脚力</span>：$kyakuryoku</td></tr>
<tr style=" border: $st_win_wak; border-style: solid; border-top-width: 1px; border-right-width: 0px; border-bottom-width: 1px; border-left-width: 0px"><td  width="25%"><span class=tyuu>◆その他</span></td>
<td><span class=honbun2>LOVE</span>：$love</td>
<td><span class=honbun2>面白さ</span>：$unique</td>
<td><span class=honbun2>エッチ</span>：$etti</td></tr>
</table>
<Script Language="JavaScript">
<!--
function bzc(){
	document.getoin.burauza_in.value = navigator.appName;
}
//-->
</Script>

<table width="100%" border="3" bordercolor="#199eff" cellspacing="0" cellpadding="5">
<form method="POST" name="getoin" action="$script">
<input type=hidden name="mode" value="login_view">
<input type="hidden" name="burauza_in" value="">
<tr bgcolor="#199eff">
<td><font color="#ffffff">●ログイン（登録済みの方）</font></td>
</tr>
<tr bgcolor="#ffffff">
<td align="left">
	$disp_tag
	名　　　前　<input type="text" name="name" size="20" value="$ck{'name'}" maxlength="20"><br>
	パスワード　<input type="text" name="pass" ssize="20" value="$ck{'pass'}" maxlength="20"><br>
	一覧で名前を
	<select name="sanka_hyouzi_on">
	<option value="on" selected>表\示する</option>
	<option value="off">表\示しない</option>
	</select><br>
	<div align="center"><input type="submit" value="街に入る" onMouseDown='bzc()'></div>
</td>
</tr>
</form>
</table>

<br><br>
</div>
	
</body></html>
EOM

	exit;
}

######データ保存
sub data_hozon {
	&lock;
	open(DH,"< $logfile") || &error("Open Error : $logfile");
	eval{ flock (DH, 2); };
		@ranking_data = <DH>;
	close(DH);
	$sonzai_flag=0;
	$i = 0;
	foreach (@ranking_data){
		&list_sprit($_);
		if ($k_id eq "$list_k_id"){
			$ranking_data[$i] = $my_prof;
			$sonzai_flag = 1;
			last;
		}
		$i ++;
#		&list_temp;
#		push (@new_ranking_data,$list_temp);
	}
	if ($sonzai_flag==0){unshift (@ranking_data,$my_prof);}
#	unshift (@new_ranking_data,$my_prof);
	
#（ver.1.40ここから）
	if ($mem_lock_num == 0){
		$err = &data_save($logfile, @ranking_data);#koko2007/07/07
		if ($err) {&error("$err");}
	}else{
		open(OUT,">$logfile") || &error("Write Error : $logfile");
		eval{ flock (OUT, 2); };
		print OUT @ranking_data;
		close(OUT);
	}
#（ver.1.40ここまで）
#フォルダー内のファイル名を取得してバックアップログを作成
#					use DirHandle;
#					$dir = new DirHandle ("./member/"."$k_id");
#ver.1.2ココから
#					$back_folder_name = "$k_id" . "backup";
#					$back_folder_pass = "./member/$back_folder_name";
#					if (! -e "./member/$back_folder_name"){
#						mkdir($back_folder_pass, 0755) || &error("Error : can not Make Directry");
#							if ($zidouseisei == 1){
#								chmod 0777,"$back_folder_pass";
#							}elsif ($zidouseisei == 2){
#								chmod 0755,"$back_folder_pass";
#							}else{
#								chmod 0755,"$back_folder_pass";
#							}
#					}
#ver.1.2ココまで
#					while($file_name = $dir->read){ #1つ読み込んで$folder_nameに代入
#							if($file_name eq '.' || $file_name eq '..' || $file_name =~ /^backup_/ || $file_name eq '.DS_Store'){next;}
#							$backup_name = "backup_" ."$file_name";
#							open (BK,"< ./member/$k_id/$file_name")  || &error("Open Error : ./member/$k_id/$file_name");
#							eval{ flock (BK, 2); };
#							@back_data = <BK>;
#							close (BK);
#							if (@back_data != ""){		#ver.1.22
#								open (BKO,">./member/$back_folder_name/$backup_name");		#ver.1.2
#								eval{ flock (BKO, 2); };
#								print BKO @back_data;
#								close (BKO);
#							}				#ver.1.22
#					}
#					$dir->close;  #ディレクトリを閉じる
#ver.1.30ここから
	open(GUEST,"< $guestfile");
	eval{ flock (GUEST, 2); };
	@all_guest=<GUEST>;
	close(GUEST);
	@new_all_guest = ();
	foreach (@all_guest) {
		($sanka_timer,$sanka_name,$hyouzi_check,$mati_name) = split(/<>/);
		if ($name eq "$sanka_name"){next;}
		chomp $mati_name;
		$sanka_tmp = "$sanka_timer<>$sanka_name<>$hyouzi_check<>$mati_name<>\n";
		push (@new_all_guest,$sanka_tmp);
	}
#ver.1.40ここから
	if ($mem_lock_num == 0){
		$err = &data_save($guestfile, @new_all_guest);#koko2007/07/07
		if ($err) {&error("$err");}
	}else{
		open(GUEST,">$guestfile");
		eval{ flock (GUEST, 2); };
		print GUEST @new_all_guest;
		close(GUEST);
	}
#ver.1.40ここまで
#ver.1.30ここまで
	&unlock;
	&set_cookie;
	&header("","sonomati");
	print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">
お疲れさまでした。
</span>
</td></tr></table>
<br>
EOM
	&hooter("login_view","戻る");
	print <<"EOM";
	<div align=center><form method=POST action="$script">
	<input type=submit value="TOPへ">
	</form></div>
EOM
	exit;
}