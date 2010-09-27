########################################2007/02/02
# 上限エンディングを働かせる。$ending_on = "1";$ending_on = ""; 上限無し
$ending_on = "";
# 株変動記録
$kabu_log_f = './log_dir/kabuhendou_log.cgi';
# 管理人メッセ流れ防止対策　#koko2007/02/05 1～$aisatu_max　までの数値 0は前のまま
$hatugenkanri = 10;
# 宣伝流れ防止対策　#koko2007/02/05 1～$aisatu_max　までの数値 0は前のまま
$hatugensenden = 10;
# 連続投稿(top) 'no' 連続投稿禁止
$renzoktoukou = 'yes';
# 挨拶集計ファイル koko2007/10/27
$aisatu_datfile  = "./log_dir/aisatu_dat.cgi";
# 挨拶のタイムスタンプ　'long','no' koko2007/10/27
$time_stanpu = 'long';
########################################
sub event_happen {
#koko2006/05/29
	if ($ending_on){
#koko 2005/03/26 上限設定
		if ($k_sousisan > 999999999999){
			$money = 0; #持ち金
			$bank = 50000000; #銀行普通
			$super_teiki = 50000000; #銀行定期
			$loan_nitigaku = 0; #ローン日額
			$loan_kaisuu = 0 ; #ローン回数

			$job_keiken =0;#経験値
			$job_kaisuu =0;#勤務数
			$job = '学生';#職　業
			$job_level =0;#$job_level

			$happend_ivent .= "<div class=purasu>●大富豪になったのでまたチャレンジしてね。</div><meta http-equiv=\"refresh\" content=\"1;URL=ending.htm\">";
			return;
		} elsif ($k_sousisan > 900000000000){ #koko2005/09/16
			$happend_ivent .= "<div class=purasu>●もうすぐ大富豪エンディング</div>";
		} #kokoend
		$max_countx =0;
		if ($looks >= 99999){$looks = 99999;$max_countx++}
		if ($tairyoku >= 99999){$tairyoku = 99999;$max_countx++}
		if ($kenkou >= 99999){$kenkou = 99999;$max_countx++}
		if ($speed >= 99999){$speed = 99999;$max_countx++}
		if ($power >= 99999){$power = 99999;$max_countx++}
		if ($wanryoku >= 99999){$wanryoku = 99999;$max_countx++}
		if ($kyakuryoku >= 99999){$kyakuryoku = 99999;$max_countx++}

		if ($kokugo >= 99999){$kokugo = 99999;$max_countx++}
		if ($suugaku >= 99999){$suugaku = 99999;$max_countx++}
		if ($rika >= 99999){$rika = 99999;$max_countx++}
		if ($syakai >= 99999){$syakai = 99999;$max_countx++}
		if ($eigo >= 99999){$eigo = 99999;$max_countx++}
		if ($ongaku >= 99999){$ongaku = 99999;$max_countx++}
		if ($bijutu >= 99999){$bijutu = 99999;$max_countx++}

		if ($love >= 99999){$love = 99999;$max_countx++}
		if ($unique >= 99999){$unique = 99999;$max_countx++}
		if ($etti >= 99999){$etti = 99999;$max_countx++}
#koko2005/09/16
		$max_countx2 =0;
		if ($looks >= 98999){$max_countx2++}
		if ($tairyoku >= 98999){$max_countx2++}
		if ($kenkou >= 98999){$max_countx2++}
		if ($speed >= 98999){$max_countx2++}
		if ($power >= 98999){$max_countx2++}
		if ($wanryoku >= 98999){$max_countx2++}
		if ($kyakuryoku >= 98999){$max_countx2++}

		if ($kokugo >= 98999){$max_countx2++}
		if ($suugaku >= 98999){$max_countx2++}
		if ($rika >= 98999){$max_countx2++}
		if ($syakai >= 98999){$max_countx2++}
		if ($eigo >= 98999){$max_countx2++}
		if ($ongaku >= 98999){$max_countx2++}
		if ($bijutu >= 98999){$max_countx2++}

		if ($love >= 98999){$max_countx2++}
		if ($unique >= 98999){$max_countx2++}
		if ($etti >= 98999){$max_countx2++}

		if ($max_countx >=17){
			$looks = int($looks/10);
			$tairyoku = int($tairyoku/10);
			$kenkou = int($kenkou/10);
			$speed = int($speed/10);
			$power = int($power/10);
			$wanryoku = int($wanryoku/10);
			$kyakuryoku = int($kyakuryoku/10);

			$kokugo = int($kokugo/10);
			$suugaku = int($suugaku/10);
			$rika = int($rika/10);
			$syakai = int($syakai/10);
			$eigo = int($eigo/10);
			$ongaku = int($ongaku/10);
			$bijutu = int($bijutu/10);

			$love = int($love/10);
			$unique = int($unique/10);
			$etti = int($etti/10);

			$happend_ivent .= "<div class=purasu>●身体・頭脳能力が天才になったのでまたチャレンジしてね。</div><meta http-equiv=\"refresh\" content=\"1;URL=ending2.htm\">";
			return;
		} elsif ($max_countx2 >=9){ #koko2005/09/16
			$happend_ivent .= "<div class=purasu>●もうすぐ天才エンディング</div>";
		}
# kokoend
	}

#2006/12/17 2007/01/05
	if (-e"./log_dir/kab_hendou.cgi"){
		if (-z "./log_dir/kab_hendou.cgi"){
#koko2007/01/07
			if (!(-e "./log_dir/kab_hendou_b.cgi")){
				$kab_dat = "25000<>25000<>25000<>25000<>25000<>0<>''<>\n";
				open(IN,">./log_dir/kab_hendou.cgi") || &error("Open Error1 : ./log_dir/kab_hendou.cgi");
				eval{ flock (IN, 2); };
				print IN $kab_dat;
				print IN @ivent_log;
				close(IN);
			}else{
				open(IN,"< ./log_dir/kab_hendou_b.cgi") || &error("Open Error2 : ./log_dir/kab_hendou.cgi");
				eval{ flock (IN, 2); };
				$kab_dat = <IN>;
				@ivent_log = <IN>;
				close(IN);
			}
#kokoend
		}else{
			open(IN,"< ./log_dir/kab_hendou.cgi") || &error("Open Error3 : ./log_dir/kab_hendou.cgi");
			eval{ flock (IN, 2); };
			$kab_dat = <IN>;
			@ivent_log = <IN>;
			close(IN);
		}
		($kabukaA,$kabukaB,$kabukaC,$kabukaD,$kabukaE,$torihiki,$torihiki_time) = split(/<>/,$kab_dat);
		open(GUEST,"< $guestfile");
		eval{ flock (GUEST, 2); };
		@all_guest=<GUEST>;
		close(GUEST);

		if ($kabukaA<=0 || $kabukaB<=0 || $kabukaC<=0 || $kabukaD<=0 || $kabukaE<=0){
	#		$stop_flag = 1;
		}
		if (($torihiki <= 0 || $torihiki_time < time()) && !$stop_flag){
			$saikoro0 = int(rand(10 * ($#all_guest+1))); #　景気
			if ($saikoro0 == 1 || $saikoro0 ==2){
				$saikoro1 = int(rand(100)+1);
				$kab_hendou = 1;
				if ($saikoro0 == 1){
					$kabu_event .= "景気よし ";
					$agene = int($kabukaA * ($saikoro1/1000) * 1.11111);
					if ($agene > 2500){$agene = 2500;}
					$kabukaA += $agene;
					$kabu_event .= "大阪 $agene,";

					$agene = int($kabukaB * ($saikoro1/1000) * 1.11111);
					if ($agene > 2500){$agene = 2500;}
					$kabukaB += $agene;
					$kabu_event .= "滋賀 $agene,";

					$agene = int($kabukaC * ($saikoro1/1000) * 1.11111);
					if ($agene > 2500){$agene = 2500;}
					$kabukaC += $agene;
					$kabu_event .= "兵庫 $agene,";

					$agene = int($kabukaD * ($saikoro1/1000) * 1.11111);
					if ($agene > 2500){$agene = 2500;}
					$kabukaD += $agene;
					$kabu_event .= "奈良 $agene,";

					$agene = int($kabukaE * ($saikoro1/1000) * 1.11111);
					if ($agene > 2500){$agene = 2500;}
					$kabukaE += $agene;
					$kabu_event .= "近畿 $agene,";

				}elsif($saikoro0 == 2){
					$kabu_event .= "景気わる ";
					$agene = int($kabukaA * ($saikoro1/1000));
					$kabukaA -= $agene;
					$kabu_event .= "大阪 -$agene,";
					$agene = int($kabukaB * ($saikoro1/1000));
					$kabukaB -= $agene;
					$kabu_event .= "滋賀 -$agene,";
					$agene = int($kabukaC * ($saikoro1/1000));
					$kabukaC -= $agene;
					$kabu_event .= "兵庫 -$agene,";
					$agene = int($kabukaD * ($saikoro1/1000));
					$kabukaD -= $agene;
					$kabu_event .= "奈良 -$agene,";
					$agene = int($kabukaE * ($saikoro1/1000));
					$kabukaE -= $agene;
					$kabu_event .= "近畿 -$agene,";
	
					if ($kabukaA < 250){
						$kabukaA =10000;
						$kabu_event .= "大阪買収統合";
					}
					if ($kabukaB < 250){
						$kabukaB =10000;
						$kabu_event .= "滋賀買収統合";
					}
					if ($kabukaC < 250){
						$kabukaC =10000;
						$kabu_event .= "兵庫買収統合";
					}
					if ($kabukaD < 250){
						$kabukaD =10000;
						$kabu_event .= "奈良買収統合";
					}
					if ($kabukaE < 250){
						$kabukaE =10000;
						$kabu_event .= "近畿買収統合";
					}
				}
			}
			#koko2006/01/14
			if ($kab_hendou != 1){
				$saikoro2 = int(rand(20*($#all_guest+1))); #
				if ($saikoro2 <= 10 && $saikoro2 != 0){
					$saikoro3 = int(rand(50)+1) / 10;
					$kab_hendou = 1;
#a
					if ($saikoro2 == 1){
						$agene = int($kabukaA * (0.05 + $saikoro3 / 100) * 1.11111) + 10;
						if ($agene > 1000){$agene = 1000;}
						$kabukaA += $agene;
						$kabu_event .= "大阪新商品成功 $agene,";
					}elsif ($saikoro2 == 2){
						$agene = int($kabukaA * (0.05 + $saikoro3 / 100));
						$kabukaA -= $agene;
						$kabu_event .= "大阪新商品失敗 -$agene,";
#b
					}elsif ($saikoro2 ==3){
						$agene = int($kabukaB * (0.05 + $saikoro3 / 100) * 1.11111) + 10;
						if ($agene > 1000){$agene = 1000;}
						$kabukaB +=  $agene;
						$kabu_event .= "滋賀新商品成功 $agene,";
					}elsif ($saikoro2 == 4){
						$agene = int($kabukaB * (0.05 + $saikoro3 / 100));
						$kabukaB -= $agene;
						$kabu_event .= "滋賀新商品失敗 -$agene,";
#c
					}elsif ($saikoro2 ==5){
						$agene = int($kabukaC * (0.05 + $saikoro3 / 100) * 1.11111) + 10;
						if ($agene > 1000){$agene = 1000;}
						$kabukaC +=  $agene;
						$kabu_event .= "兵庫新商品成功 $agene,";
					}elsif ($saikoro2 == 6){
						$agene = int($kabukaC * (0.05 + $saikoro3 / 100));
						$kabukaC -= $agene;
						$kabu_event .= "兵庫新商品失敗 -$agene,";
#d
					}elsif ($saikoro2 ==7){
						$agene = int($kabukaD * (0.05 + $saikoro3 / 100) * 1.11111) + 10;
						if ($agene > 1000){$agene = 1000;}
						$kabukaD +=  $agene;
						$kabu_event .= "奈良新商品成功 $agene,";
					}elsif ($saikoro2 == 8){
						$agene = int($kabukaD * (0.05 + $saikoro3 / 100));
						$kabukaD -= $agene;
						$kabu_event .= "奈良新商品失敗 -$agene,";
#e
					}elsif ($saikoro2 ==9){
						$agene = int($kabukaE * (0.05 + $saikoro3 / 100)* 1.11111) + 10;
						if ($agene > 1000){$agene = 1000;}
						$kabukaE +=  $agene;
						$kabu_event .= "近畿新商品成功 $agene,";
					}elsif ($saikoro2 == 10){
						$agene = int($kabukaE * (0.05 + $saikoro3 / 100));#kokodame
						$kabukaE -= $agene;
						$kabu_event .= "近畿新商品失敗 -$agene,";
					}
				}
			}
			if ($kab_hendou == 1){
				unshift @ivent_log,"$in{'name'}さんの努力により$kabu_event<br>\n";
				if ($#ivent_log + 1 >=30){$#ivent_log =29;}

				open (IN, "> ./log_dir/kab_hendou.cgi") || &error("Open Error4 : ./log_dir/kab_hendou.cgi");
				eval{ flock (IN, 2); };
				print IN "$kabukaA<>$kabukaB<>$kabukaC<>$kabukaD<>$kabukaE<>0<>$torihiki_time<>\n";
				print IN @ivent_log;
				close (IN);

				open (IN, "> ./log_dir/kab_hendou_b.cgi") || &error("Open Error5 : ./log_dir/kab_hendou_b.cgi");
				eval{ flock (IN, 2); };
				print IN "$kabukaA<>$kabukaB<>$kabukaC<>$kabukaD<>$kabukaE<>0<>$torihiki_time<>\n";
				print IN @ivent_log;
				close (IN);
			}
		}
	}

	if($in{'goki'} eq "on"){
		$now_goki = time;
		if($in{'goki_time'} + 15 > $now_goki){
			$syou_rand = int(rand(20000))+1;
			$happend_ivent .= "<div class=purasu>●ゴキブリを手で潰しました。<br>　  謝礼金$syou_rand円とＫポイント３Ｐもらえました。</div><div class=mainasu>　ルックスが３下がりました。</div>";
			$money += $syou_rand;
			$kpoint += 3;
			$looks -= 3;
			&event_kiroku($in{'name'},$happend_ivent);
  		}else{
			$happend_ivent .= "<div class=mainasu>ゴキブリに逃げられてしまった・・・。残念！</div>";
  		}
	}
	
	#&motimono_kensa("胃弁当");
	if ($kensa_flag == 1){$hassei_rand = int(rand(5))+1;}
	else{$hassei_rand = int(rand(5))+1;}
	
	if ($hassei_rand ==1){
		$event_rand = int(rand(46))+1;
		#$event_rand = "44";	#限定イベント
		
		if ($event_rand == 1){
			$syou_rand = int(rand(100000))+1;
			if (int(rand(2))+1 == 1){
				if ($money <= 0){
					$happend_ivent .= "<div class=purasu>●お正月早々、スリに遭いましたが、盗むお金が無かったので捨てぜりふを残して立ち去りました。</div>";
				}else{
					$happend_ivent .= "<div class=purasu>●お正月早々、スリに遭いましたが返してくれました。</div>";
				}
			}else{
				$money += $syou_rand;
				$happend_ivent .= "<div class=purasu>●お正月早々、スリを捕まえました。<br>　  謝礼金$syou_rand円がもらえました。</div>";
			}
		}
			
		if ($event_rand == 2){
			$syou_rand = int(rand(10000))+1;
			$happend_ivent .= "<div class=purasu>●お正月早々、道でお財布を拾いました。<br>　  $syou_rand円入っていたのでやっぱりねこばばしました。</div>";
			$money += $syou_rand;
		}
			
		if ($event_rand == 3){
			if (int(rand(2))+1 == 1){
				$happend_ivent .= "<div class=purasu>●お正月早々、宣教師に出会い、親しげに話しかけられたうえ、英語を教えてくれました。<br>　  英語力３アップ！</div>";
				$eigo += 3;
				&motimono_kensa_ev("英文解釈教室");
				if ($kensa_flag == 1){
					$happend_ivent .= "<div class=purasu>●また、英文解釈教室を持っていたところを見つかり、さらに熱心に教えてくれました。<br>　  英語力5アップ！</div>";
					$eigo += 5;
				}
			}else{
				$happend_ivent .= "<div class=mainasu>●お正月早々、英語の先生に見放されました。<br>　  英語力３ダウン！</div>";
				$eigo -= 3;
			}
		}
			
		if ($event_rand == 4){
			$happend_ivent .= "<div class=mainasu>●お正月早々、風邪を引いてしまいました。</div>";
			$byouki_sisuu = -15;
		}

		if ($event_rand == 5){
			$happend_ivent .= "<div class=mainasu>●お正月早々、NHKの集金がやってきました。<br>　  1000円払いました。</div>";
			$money -= 1000;
		}

		if ($event_rand == 6){
			$happend_ivent .= "<div class=purasu>●お正月早々、失恋してやけ食いしました。<br>　  体重が５kg増えました。</div>";
			$taijuu += 5;
		}

		if ($event_rand == 7){
			if (int(rand(2))+1 == 1){
				$happend_ivent .= "<div class=purasu>●お正月早々、文学に目覚めました。<br>　  国語力３アップ！</div>";
				$kokugo += 3;
			}else{
				$happend_ivent .= "<div class=mainasu>●お正月早々、パ\ソ\コンばかりして漢字を忘れてしまいました。<br>　  国語力３ダウン！</div>";
				$kokugo -= 3;
			}
		}

		if ($event_rand == 8){
			if (int(rand(2))+1 == 1){
				$happend_ivent .= "<div class=purasu>●お正月早々、数学パズルで遊びました。<br>　  数学力３アップ！</div>";
				$suugaku += 3;
			}else{
				$happend_ivent .= "<div class=mainasu>●お正月早々、数字恐怖症になりました。<br>　  数学力３ダウン！</div>";
				$suugaku -= 3;
			}
		}

		if ($event_rand == 9){
			if (int(rand(2))+1 == 1){
				$happend_ivent .= "<div class=purasu>●お正月早々、テレビで科学の番組を見ました。<br>　  理科の力が３アップ！</div>";
				$rika += 3;
			}else{
				$happend_ivent .= "<div class=mainasu>●お正月早々、理科の実験で試験管を割ってしまいました。<br>　  理科の力が３ダウン！</div>";
				$rika -= 3;
			}
		}

		if ($event_rand == 10){
			if (int(rand(2))+1 == 1){
				$happend_ivent .= "<div class=purasu>●お正月早々、歴史の本を読みました。<br>　  社会の力が３アップ！</div>";
				$syakai += 3;
			}else{
				$happend_ivent .= "<div class=mainasu>●お正月早々、社会への関心が引き潮が引くように無くなっていきました。<br>　  社会の力が３ダウン！</div>";
				$syakai -= 3;
			}
		}

		if ($event_rand == 11){
			if (int(rand(2))+1 == 1){
				$happend_ivent .= "<div class=purasu>●お正月早々、ピアノの練習をしました。<br>　  音楽の力が３アップ！</div>";
				$ongaku += 3;
			}else{
				$happend_ivent .= "<div class=mainasu>●お正月早々、飲み会で騒ぎすぎガラガラ声になりました。<br>　  音楽の力が３ダウン！</div>";
				$ongaku -= 3;
			}
			&motimono_kensa_ev("成り上がり");
			if ($kensa_flag == 1){
				$happend_ivent .= "<div class=purasu>●お正月早々、「成り上がり」を読んで音楽へのやる気がわいてきました。<br>　  音楽5アップ</div>";
				$ongaku += 3;
			}
		}

		if ($event_rand == 12){
			if (int(rand(2))+1 == 1){
				$happend_ivent .= "<div class=purasu>●お正月早々、芸術に目覚めました。<br>　  美術の力が３アップ！</div>";
				$bijutu += 3;
			}else{
				$happend_ivent .= "<div class=mainasu>●お正月早々、美術の授業で居眠りをしてしまいました。<br>　  美術の力が３ダウン！</div>";
				$bijutu -= 3;
			}
		}

		if ($event_rand == 13){
			$kuzi_rand = int(rand(15))+1;
			$kuzi_gaku = $kuzi_rand * 10000;
			$happend_ivent .= "<div class=purasu>●お正月早々、ラッキーくじが当たりました！<br>　  $kuzi_rand万円ゲット！</div>";
			$money += $kuzi_gaku;
		}
			
		if ($event_rand == 14){
			$happend_ivent .= "<div class=purasu>●お正月早々、不思議に優しい気持ちにつつまれました。<br>　  LOVE度が５アップ！</div>";
			$love += 5;
		}

		if ($event_rand == 15){
			$happend_ivent .= "<div class=mainasu>●お正月早々、裸で寝ていたら体調を崩したようです。</div>";
			$byouki_sisuu = -8;
		}

		if ($event_rand == 16){
			&motimono_kensa_ev("防犯カメラ");
		if($bank <= 0){
				$happend_ivent .= "<div class=mainasu>●お正月早々、空き巣が入りましたが、「ちっ、ここには金がねぇ。。」<br>  と言って出て行きました。</div>";
			}elsif ($kensa_flag == 1){
			if (int(rand(5))+1 == 1){
			&motimono_kensa_ev2("防犯カメラ");
				$happend_ivent .= "<div class=mainasu>●お正月早々、空き巣が入りましたが、防犯カメラが壊されてました。<br>  通帳を盗られ、普通口座の預け入れ額が５分の１減ってしまいました。</div>";
				$bank2=int ($bank / 5);
				$bank -= $bank2;
			&kityou_syori("空き巣","$bank2","",$bank,"普");
				}else{
			$money+=100000;
				$happend_ivent .= "<div class=purasu>●お正月早々、空き巣が入りましたが、防犯カメラがあったので捕まえることができました。<br>　  （謝礼金がもらえました）</div>";
				}
				
				}elsif(int(rand(2))+1 == 1){
				$happend_ivent .= "<div class=mainasu>●お正月早々、空き巣に遭いましたが近所の人が捕まえました。</div>";
				}else{
				$happend_ivent .= "<div class=mainasu>●お正月早々、空き巣に遭いました。<br>　  通帳を盗られ、普通口座の預け入れ額が５分の１減ってしまいました。</div>";
				$bank2=int ($bank / 5);
				$bank -= $bank2;
			&kityou_syori("空き巣","$bank2","",$bank,"普");
				}
		}

		if ($event_rand == 17){
			$myranded=int(rand(2))+1;
			&motimono_kensa_ev("おばあちゃんの知恵袋");
			if ($kensa_flag == 1){
				$happend_ivent .= "<div class=purasu>●お正月早々、おばあちゃんの知恵をまとめて出した本の印税が3000円入りました。</div>";
				$money=$money+3000;
			}elsif($myranded == 1){
				$happend_ivent .= "<div class=purasu>●お正月早々、出した本の印税が1000円入りました。</div>";
				$money=$money+1000;
			}else{
				$happend_ivent .= "<div class=purasu>●お正月早々、出した本の印税が500円入りました。</div>";
				$money=$money+500;
			}
		}

		if ($event_rand == 18){
			$myranded=int(rand(2))+1;
			&motimono_kensa_ev("フラフープ");
			if ($kensa_flag == 1){
				$happend_ivent .= "<div class=purasu>●お正月早々、家にあったフラフープがハッピーな出来事を運んできたようです！<br>　  家の前に77777円落ちてました。</div>";
				$money=$money+77777;
			}elsif($myranded == 1){
				$happend_ivent .= "<div class=purasu>●お正月早々、家の前に5000円落ちてました。</div>";
				$money=$money+100;
			}else{
				$happend_ivent .= "<div class=mainasu>●お正月早々、前に財布をねこばばした事がばれて逆に500円払いました。</div>";
				$money=$money-500;
			}
		}

		if ($event_rand == 19){
			&motimono_kensa_ev("谷保天満宮のお守り");
			if ($kensa_flag == 1){
				$happend_ivent .= "<div class=purasu>●お正月早々、車にひかれかけましたが『谷保天満宮のお守り』が守ってくれ、さらに謝罪費として3万をもらうことができました。</div>";
				$money=$money+30000;
			}elsif($speed <= 180){
				$happend_ivent .= "<div class=mainasu>●お正月早々、車にひかれて軽いケガを負いました。<br>　  入院費として３万円かかりました。</div>";
				$money=$money-30000;
			}else{
				$happend_ivent .= "<div class=purasu>●お正月早々、車にひかれかけましたが、軽いフットワークでかわしました。</div>";
			}
		}

		if ($event_rand == 20){
			$myranded=int(rand(2))+1;
			&motimono_kensa_ev("幸せを呼ぶ香水");
			if ($kensa_flag == 1){
				$happend_ivent .= "<div class=purasu>●お正月早々、家にあった「幸せを呼ぶ香水」が持ち金を倍にしてくれました！</div>";
				$money=$money * 2;
			}elsif($myranded == 1){
				$happend_ivent .= "<div class=purasu>●お正月早々、家の前に１万円落ちてました。</div>";
				$money=$money+100000;
			}else{
				$happend_ivent .= "<div class=mainasu>●お正月早々、パチンコで１万すってしまいました。。</div>";
				$money=$money-10000;
			}
		}

		if ($event_rand == 21){
			$myranded=int(rand(2))+1;
			&motimono_kensa_ev("バイアグラ");
			if ($kensa_flag == 1){
				$happend_ivent .= "<div class=purasu>●お正月早々、家にあった「バイアグラ」を使ってLOVE度＆エッチ度３アップ！</div>";
				$love += 3;
				$etti += 3;
			}elsif($myranded == 1){
				$happend_ivent .= "<div class=purasu>●お正月早々、友人がこっそりスッポンエキスを送ってきてくれました。<br>　  エッチ度３アップ！</div>";
				$etti += 3;
			}else{
				$happend_ivent .= "<div class=mainasu>●お正月早々、下痢気味でエッチにも力が入りません。。<br>　  エッチ度３ダウン。。</div>";
				$etti -= 3;
			}
		}

		if ($event_rand == 22){
			&motimono_kensa_ev("損害保険");
			if ($kensa_flag == 1){
				$happend_ivent .= "<div class=mainasu>●お正月早々、地震が発生しました！！<br>　  が、損害保険のおかげで全額保障されました。</div>";
			}elsif (int(rand(2))+1 == 1){
				$happend_ivent .= "<div class=mainasu>●お正月早々、地震が発生しました！！<br>　　と、思ったら<s>エネゴリ君</s>目を回していただけでした。</div>";
			}else{
				$happend_ivent .= "<div class=purasu>●お正月早々、資産運用に成功して持ち金が倍になりました。</div>";
				$syushitu = $money;
				$money = int ($money*2);
				&news_kiroku("運用","$in{'name'}さんが、資産運用に成功して$syushitu円儲けました。");
			}
		}
        
		if ($event_rand == 23){
			$myranded=int(rand(4))+1;
			&motimono_kensa_ev("ブラタンメンバーズカード");
			if ($kensa_flag == 1){
				if ($myranded == 1){
					$happend_ivent .= "<div class=purasu>●お正月特典♪<br>　  現金1万円が当たりました！</div>";
					$money += 10000;
				}elsif ($myranded == 2){
					$happend_ivent .= "<div class=purasu>●お正月特典♪<br>　  現金10万円が当たりました！</div>";
					$money += 100000;
				}elsif ($myranded == 3){
						$happend_ivent .= "<div class=purasu>●お正月特典♪<br>　  現金50万円が当たりました！</div>";
					$money += 500000;
				}elsif ($myranded == 4){
					$happend_ivent .= "<div class=purasu>●お正月特典♪<br>　  現金100万円が当たりました！</div>";
					$money += 1000000;
				}
			}else{
				$in{'town_no'}=int(rand(3));
				$happend_ivent .= "<div class=mainasu>●お正月早々、ＵＦＯにさらわれて$town_hairetu[$in{'town_no'}]へ飛ばされてしまいました！！</div>";
			}
		}

		if ($event_rand == 24){
			if (int(rand(10))+1 == 1){
				$kuzi_rand = int(rand(10))+1;
				$kuzi_gaku = $kuzi_rand * 1000000;
				$kuzi_hyouzi = $kuzi_rand . "00";
				$happend_ivent .= "<div class=purasu>●お正月早々、宝くじが当たりました！<br>　  $kuzi_hyouzi万円ゲット！</div>";
				$money += $kuzi_gaku;
			}else{
				$happend_ivent .= "<div class=mainasu>●お正月早々、宝くじを3000円分購入しましたがやっぱり外れました。</div>";
				$money -= 3000;
			}
		}

		if ($event_rand == 25){
			$happend_ivent .= "<div class=mainasu>●お正月早々、大阪のおばちゃんに説教されてノイローゼになりました。<br>　  体重が1kg減りました。</div>";
			$taijuu -= 1;
		}
        
		if ($event_rand == 26){
			$my_rand = int(rand(5))+1;
			if ($my_rand == 1){
				$energy -= int($energy / 3);
				$happend_ivent .= "<div class=mainasu>●お正月早々、ストリートファイトの巻き添えで、身体パワーが１/３減らされた。</div>";
			}elsif ($my_rand == 2){
				$nou_energy -= int($nou_energy / 3);
				$happend_ivent .= "<div class=mainasu>●お正月早々、ストリートファイトの巻き添えで、頭脳パワーが１/３減らされた。</div>";
			}elsif ($my_rand == 3){
				$energy -= int($energy / 4);
				$nou_energy -= int($nou_energy / 4);
				$happend_ivent .= "<div class=mainasu>●お正月早々、ストリートファイトの巻き添えで、身体パワー・頭脳パワーが１/４減らされた。</div>";
			}else{
				$happend_ivent .= "<div class=purasu>●お正月早々、ストリートファイトが起こりそうなので逃げ出して事なきを得た。</div>";
			}
		}
        
		if ($event_rand == 27){
			$energy += 1000;
			$nou_energy += 1000;
			$happend_ivent .= "<div class=purasu>●お正月早々、温泉の入浴券をもらって身体・頭脳パワーが1000回復しました。</div>";
		}
        
		if ($event_rand == 28){
			$okane = 10000;
			&kifu;
		}
        
		if ($event_rand == 29){
			&motimono_kensa_ev("幸せの星砂");
			if ($kensa_flag == 1){
				$happend_ivent .= "<div class=purasu>●お正月早々、家にあった「幸せの星砂」が持ち金を倍にしてくれました！</div>";
				$money = int ($money*2);
			}else{
				$happend_ivent .= "<div class=purasu>●お正月早々、家の前に１万円落ちてました。</div>";
				$money += 10000;
			}
		}
        
		if ($event_rand == 30){
			$my_rand = int(rand(5))+1;
			&coupon_get($my_rand);
			$happend_ivent .= "<div class=purasu>●お正月早々、クーポン券を $my_randつもらいました！</div>";
		}
        
		if ($event_rand == 31){
			&motimono_kensa_ev("ミグ25");
			if ($kensa_flag == 1){
				$happend_ivent .= "<div class=mainasu>●お正月早々、グレムリンに悪戯された。<br>　  ミグ25の耐久が$dsp_syo_taikyuuになった！</div>";
			}else{
				$happend_ivent .= "<div class=purasu>●お正月早々、自動販売機に100円入ってました。</div>";
				$money += 100;
			}
		}
        
		if ($event_rand == 32){
			&motimono_kensa_ev2("小さな花束(ラン)","ルパン三世","ファイナルクエスト");
			if ($kensa_flag == 1){
				$happend_ivent .= "<div class=mainasu>●お正月早々、必要な品物を持っていました。</div>";
				$money += 100000;
			}else{
				$happend_ivent .= "<div class=purasu>●お正月早々、５０００円拾った。</div>";
				$money += 500000;
			}
		}
        
		if ($event_rand == 33){
			$my_rand = int(rand(3))+1;
			if ($my_rand == 1){
				$happend_ivent .= "<div class=purasu>●お正月早々、吉本の芸人に出会いました。<br>　  面白さが３アップ！</div>";
				$unique += 3;
			}elsif ($my_rand == 2){
				$energy -= int($energy / 3);
				$happend_ivent .= "<div class=mainasu>●お正月早々、奈良で鹿に踏まれて、身体パワーが１/３減らされました。</div>";
			}else{
				$energy -= int($energy / 2);
				$happend_ivent .= "<div class=mainasu>●お正月早々、琵琶湖でおぼれました。<br>　  身体パワーが１/２になり、救助代５万円を払いました</div>";
				$money=$money-50000;
			}
		}
		
		if ($event_rand == 34){
			$myranded=int(rand(2))+1;
			&motimono_kensa_ev2("等身大サンタさん人形");
			if ($kensa_flag == 1){
				if ($myranded == 1){
				$happend_ivent .= "<div class=purasu>●お正月早々、サンタさんがやってきて人形と交換に持ち金を２倍にしてくれました！</div>";
				$money = int ($money*2);
				}else{
			$energy += 10000;
			$nou_energy += 10000;
				$happend_ivent .= "<div class=purasu>●お正月早々、サンタさんがやってきて身体・頭脳パワーを10000回復してもらいました。</div>";
				}
			}elsif($money <= 0){
				$money = 0;
				$happend_ivent .= "<div class=purasu>●お正月早々、徳政令が発令されました。</div>";
			}else{
				$happend_ivent .= "<div class=mainasu>お正月早々、ゴキブリだ！１０秒以内に潰せ！</div>";
				$goki="on";
			}
		}

		if ($event_rand == 35){
			$myranded=int(rand(4))+1;
			&motimono_kensa_ev2("４次元福袋");
			if ($kensa_flag == 1){
				if ($myranded == 1){
				$happend_ivent .= "<div class=purasu>●お正月早々、４次元福袋の中から１億円が出てきました！！</div>";
					$money += 100000000;
				}elsif ($myranded == 2){
			$energy += 10000;
			$nou_energy += 10000;
				$happend_ivent .= "<div class=purasu>●お正月早々、４次元福袋の中に温泉券が１０枚入ってました。<br>　  身体・頭脳パワーが10000回復しました。</div>";
				}elsif ($myranded == 3){
			$my_rand2 = int(rand(15))+1;
			&coupon_get($my_rand2);
			$happend_ivent .= "<div class=purasu>●お正月早々、４次元福袋の中にクーポン券が $my_rand2枚入ってました！</div>";
				}
			}else{
				$happend_ivent .= "<div class=mainasu>●お正月早々、サンタさんを見たと騒いで罰金１万円を払わされました。</div>";
				$money=$money-10000;
			}
		}

		if ($event_rand == 36){
		$money_aku=int(rand(50000))+1;
		$money_aku2=$money_aku*2;
			&motimono_kensa_ev("悪魔の笛");
			if ($kensa_flag == 1){
			if (int(rand(2))+1 == 1){
			$okane = $money_aku2;
			&kifu2;
			}else{
				$happend_ivent .= "<div class=mainasu>●お正月早々、悪魔の笛を吹いたら$money_aku2円なくなりました。</div>";
				$money=$money-$money_aku2;
				}
			}else{
				$happend_ivent .= "<div class=mainasu>●お正月早々、悪魔に$money_aku円すられました。</div>";
				$money=$money-$money_aku;
			}
		}
        
		if ($event_rand == 37){
		$money_ten=int(rand(10000))+1;
		$money_ten2=$money_ten*2;
			&motimono_kensa_ev("天使の笛");
			if ($kensa_flag == 1){
			$myranded=int(rand(2))+1;
			if ($myranded == 1){
			$okane = $money_ten2;
			&kifu3;
			}else{
				$happend_ivent .= "<div class=purasu>●お正月早々、天使の笛を吹いたら$money_ten2円持ち金が増えました。</div>";
				$money=$money+$money_ten2;
				}
			}else{
				$happend_ivent .= "<div class=purasu>●お正月早々、天使から$money_ten円もらいました。</div>";
				$money=$money+$money_ten;
			}
		}
        
		if ($event_rand == 38){
			if($power >= 1000){
				if(int(rand(5))+1 == 1){
					$my_rand = int(rand(6));
					&get_itm2($my_rand);
					if($kensa_flag == 2){
						$happend_ivent .= "<div class=mainasu>●お正月早々、サンタを倒したが持ち物が多くて手に入れられなかった。</div>";
					}else{
						$happend_ivent .= "<div class=purasu>●お正月早々、サンタを倒して$syo_hinmoku0を手に入れた。</div>";
					}
				}else{
					$money=$money+10000;
					$happend_ivent .= "<div class=purasu>●お正月早々、サンタと戦って、10000円ゲットしました。</div>";
				}
			}else{
				$energy = 0;
				$happend_ivent .= "<div class=mainasu>●お正月早々、サンタと戦ったが負けて身体POWERが０になった</div>";
			}
		}
		
		if ($event_rand == 39){
			if ($energy >= 500 && $nou_energy >= 500){
				$happend_ivent .= "<div class=purasu>●お正月早々、仕事にとても集中できました。仕事経験地１０うｐ！</div>";
				$job_keiken = $job_keiken+10;
			}else{
				$happend_ivent .= "<div class=mainasu>●お正月早々、疲れていて仕事に集中できません。仕事経験地５ダウン</div>";
				$job_keiken = $job_keiken-5;
			}
		}

		if ($event_rand == 40){
			$my_rand = int(rand(2));
			&get_itm($my_rand);
			if(int(rand(5))+1 == 1){
				if($kensa_flag == 2){
					$happend_ivent .= "<div class=mainasu>●お正月早々、持ち物が多くて手に入れられなかった。</div>";
				}else{
					$happend_ivent .= "<div class=purasu>●お正月早々、$syo_hinmoku0を手に入れた。</div>";
				}
			}else{
				$money=$money-500;
				$happend_ivent .= "<div class=mainasu>●お正月早々、500円を川の中に落としてしまった！</div>";
			}
		}
        
		if ($event_rand == 41){
			$happend_ivent .= "<div class=purasu>●お正月早々、自動販売機のおつり取り忘れを発見！<br>	１０００円拾いました。</div>";
			$money=$money+1000;
		}
		
		if ($event_rand == 42){
			$myranded=int(rand(2))+1;
			&motimono_kensa_ev2("阪神タイガースの公式チケット");
			if ($kensa_flag == 1){
				if($myranded==1){
					$energy=$energy-10000;
					$happend_ivent .= "<div class=mainasu>●お正月早々、阪神タイガースの応援に行き巨人ファンと乱闘を起こしました。身体パワーダウン！</div>";
				}else{
					$nou_energy=$nou_energy+100000;
					$happend_ivent .= "<div class=purasu>●お正月早々、阪神タイガースに応援に行ったら快勝しました！<br>　  頭脳パワーうｐ！</div>";
				}
			}elsif($myranded==1){
				$tairyoku=$tairyoku+10;
				$kenkou=$kenkou+10;
				$speed=$speed+10;
				$power=$power+10;
				$wanryoku=$wanryoku+10;
				$kyakuryoku=$kyakuryoku+10;
				$energy=$energy-5000;
				$happend_ivent .= "<div class=purasu>●お正月早々、タイガースの選手に出会って、特訓させられました！<br>　  身体パワーダウン、能\力うｐ！</div>";
			}else{
				$happend_ivent .= "<div class=mainasu>●お正月早々、道でこけた拍子に持ち金を半分川に落としてしまいました・・・</div>";
				$money=int($money / 2);
			}
		}

		if ($event_rand == 43){
			$happend_ivent .= "<div class=mainasu>●お正月早々、失恋して食べ物が喉を通らなくなりました。<br>　  5キロ痩せました。</div>";
			$taijuu -= 5;
		}
		
		if ($event_rand == 44){
			$happend_ivent .= "<div class=mainasu>お正月早々、ゴキブリだ！１０秒以内に潰せ！</div>";
			$goki="on";
		}
		
		if($event_rand == 45){
			$happend_ivent .= "<div class=mainasu>●お年玉が落ちてきました。</div>";
            $money += 100000;
		}
		
		if($event_rand == 46){
			$happend_ivent .= "<div class=mainasu>●初夢を見れなかった・・・ショック！</div>";
			$nou_energy -= 100000;
		}
		
		if($event_rand == 46){
			$happend_ivent .= "<div class=mainasu>●初日の出を拝んでいたらみるみる力がわいてきました！</div>";
			$energy += 100000;
		}
		
		&event_kiroku($in{'name'},$happend_ivent);

		if($otdashi eq "yes"){
			$happend_ivent .= <<"EOM";
			<OBJECT classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,0,0" WIDTH="5" HEIGHT="5" id="happen">
			<PARAM NAME=movie VALUE="$img_dir/happen.swf"> <PARAM NAME=loop VALUE=false> <PARAM NAME=quality VALUE=low> <PARAM NAME=wmode VALUE=transparent> <PARAM NAME=bgcolor VALUE=#ffffaa> <EMBED src="$img_dir/happen.swf" loop=false quality=low wmode=transparent bgcolor=#ffffaa  WIDTH="5" HEIGHT="5" NAME="happen" TYPE="application/x-shockwave-flash" PLUGINSPAGE="http://www.macromedia.com/go/getflashplayer"></EMBED>
			</OBJECT>
EOM
		}
	}else{print "";}
    
}

####挨拶
sub aisatu {
	my(@all_data,$a_total_kizisuu,$top);
	if (length($in{'a_com'}) > 200) {&error("挨拶は100字以内です");}
	if ($in{'a_com'} eq "") {&error("コメントが入力されていません");}
	&lock;
	
	# ログを読み込み
	open(IN,"< $aisatu_logfile") || &error("Open Error : $aisatu_logfile");
	eval{ flock (IN, 2); };
	$top = <IN>;
	@all_data = <IN>;
	$a_total_kizisuu = @all_data;
	local($a_num,$a_name,$a_date,$a_com,$a_syurui,$ie_link,$a_jynken_mes)= split(/<>/, $top);
	close(IN);
	
	#関西弁に整形
	if ($in{'kansai'}){
		open(IN,"dat_dir/kansai.cgi") || &error("Open Error : dat_dir/kansai.cgi");
		eval{ flock (IN, 2); };
		foreach(<IN>){
			chomp $_;
			($mae,$ato)=split(/<>/);
			$in{'a_com'} =~ s/$mae/$ato/g;
		}
		close(IN);
	}
	
	#整形
	$in{'a_com'} = &tag($in{'a_com'});
	
	#宣伝、管理人のとき
	if ($in{'a_syurui'} eq '宣伝'){
		$in{'a_com'} = "<font color=\"#0000ff\">$in{'a_com'}</font>";
	}
	if ($in{'a_syurui'} eq '管理人'){
		$in{'a_com'} = "<font color=\"#ff0000\">$in{'a_com'}</font>";
	}
	if ($in{'a_syurui'} eq '副管理人'){
		$in{'a_com'} = "<font color=\"#00ff00\">$in{'a_com'}</font>";
	}
    
    #二重、連続禁止
	if ($in{'name'} eq $a_name && $in{'a_com'} eq $a_com) {
		&error("二重投稿です");
	}
	if($in{'name'} eq $a_name){
		if($renzoktoukou eq 'no'){
			&error("連続投稿");
		}
		$renzoku ="yes";
	}
    
    #ジャンケン時の処理
	if ($in{'a_syurui'} eq "ジャンケン"){
		if(int(rand(3))+1 == 1){
			$jynken_mes = "ジャンケンで<font color=#ff0000>勝ち</font>でした。<br>";
			$janken="勝ち";
		}elsif(int(rand(3))+1 == 2){
			$jynken_mes = "ジャンケンで<font color=#0000ff>負け</font>でした。<br>";
			$janken="負け";
		}else{
			$jynken_mes = "ジャンケンで<font color=#00ff00>あいこ</font>でした。<br>";
			$janken="あいこ";
		}
	}
	
    &time_get;
	#更新配列を定義
	$a_num ++;
    
    #家へのリンク
	open(OI,"< $ori_ie_list") || &error("Open Error : $ori_ie_list");
	eval{ flock (OI, 2); };
	@ori_ie_hairetu = <OI>;
	close(OI);
	$ie_link = "";
	foreach (@ori_ie_hairetu) {
		&ori_ie_sprit($_);
		if ($k_id eq $ori_k_id){
			$ie_link = "<input type=hidden name=ori_ie_id value=\"$ori_k_id\">";
			last;
		}
	}
	
	#ログ作成
	if($time_stanpu eq 'long'){
		$a_toukou = "$a_num<>$in{'name'}<>（$date1）<>$in{'a_com'}<>$in{'a_syurui'}<>$ie_link<>$jynken_mes<>\n";
	}else{
		$a_toukou = "$a_num<>$in{'name'}<>（$date2）<>$in{'a_com'}<>$in{'a_syurui'}<>$ie_link<>$jynken_mes<>\n";
	}
            
	if ($hatugenkanri != 0){
		unshift @all_data,$top;
		@tokubetu = ();
		@ittupan = ();
		foreach (@all_data){
			(@temp) = split(/<>/);
			if ($temp[4] eq '管理人' || $temp[4] eq '副管理人'){
				push @kanrinin,$_;
			}elsif($temp[4] eq '宣伝'){
				push @senden,$_;
			}else{
				push @ittupan,$_;
			}
		}

		if ($in{'a_syurui'} eq '管理人' || $in{'a_syurui'} eq '副管理人'){
			unshift @kanrinin,$a_toukou;
			if ($#kanrinin >= $hatugenkanri-1){
				$#kanrinin = $hatugenkanri-1;
			}
			@new_all_data =(@kanrinin,@senden,@ittupan);
		}elsif($in{'a_syurui'} eq '宣伝'){
			unshift @senden,$a_toukou;
			if ($#senden >= $hatugensenden-1){
				$#senden = $hatugensenden-1;
			}
			@new_all_data =(@kanrinin,@senden,@ittupan);
		}else{
			@new_all_data = (@kanrinin,@senden,@ittupan);
			unshift @new_all_data,$a_toukou;
			if ($#new_all_data + 1 >= $aisatu_max){
				$#new_all_data = $aisatu_max - 1;
			}
		}
	}else{
		@new_all_data = ();
		$new_all_data[0] = $a_toukou;
		$new_all_data[1] = $top;
		$i = 0;
		foreach (@all_data){
			$i ++ ;
			push (@new_all_data,$_);
			if ($i >= $aisatu_max - 2){last;}
		}
	}
	
	# ログを更新
	open(OUT,">$aisatu_logfile") || &error("Write Error : $aisatu_logfile");
	eval{ flock (OUT, 2); };
	print OUT @new_all_data;
	close(OUT);
	
	# ロック解除
	&unlock;
    
	if ($in{'a_syurui'} eq '宣伝'){
		$money -=20000;
		$happend_aisatu .= '宣伝費に２万円はらいました。';
	}elsif ($in{'a_syurui'} eq '管理人'){
		$happend_aisatu .= '管理発言しました。';
	}elsif ($in{'a_syurui'} eq '副管理人'){
		$happend_aisatu .= '副管理発言しました。';
	}elsif($renzoku ne "yes"){
		#お金をゲット
		$randed += int(rand(7))+1;
		if ($randed == 7){
			$randed += int(rand(10000)) + 5000;
			if($in{'a_syurui'} eq "ジャンケン"){
				if ($janken eq "勝ち"){
					$janken_syo = '<font color="#ff0000">勝って</font>倍の';
					$randed += $randed;
				}elsif ($janken eq "負け"){
					$janken_syo = '<font color="#0000ff">負けて</font>半分の';
					$randed -= int($randed / 2);
				}else{
					$janken_syo = '<font color="#00ff00">あいこ</font>で';
				}
			}
			$money += $randed;
			$happend_aisatu .= "ボーナスがでました！$janken_syo$randed円もらいました。<br>";
		}else{
			$randed += int(rand(5000)) + 2500;
			if($in{'a_syurui'} eq "ジャンケン"){
				if ($janken eq "勝ち"){
					$janken_syo = '<font color="#ff0000">勝って</font>倍の';
					$randed += $randed;
				}elsif ($janken eq "負け"){
					$janken_syo = '<font color="#0000ff">負けて</font>半分の';
					$randed -= int($randed / 2);
				}else{
					$janken_syo = '<font color="#00ff00">あいこ</font>で';
				}
			}
			$money += $randed;
			$happend_aisatu .= "$janken_syo$randed円もらいました。<br>";
		}
	}else{
		$happend_aisatu .= "連続投稿なのでお金もらえません。";
	}

	$hatugen++;
	# ランキング用ファイル控え
	open(IN,"< $aisatu_datfile") || &error("Open Error : $aisatu_detfile");
	eval{ flock (IN, 2); };
	@aisatu_data = <IN>;
	close(IN);
	
	$aru = 0;
	$ima_time = time;
	$i = 0;
	foreach (@aisatu_data) {
		($ai_id,$ai_name,$ai_kaisu,$ai_time) = split(/<>/);
		if($ai_name eq $in{'name'}){
			$aisatu_data[$i] = "$ai_id<>$ai_name<>$hatugen<>$ima_time<>\n";
			$aru = 1;
			last;
		}
		$i++;
	}
	if(!$aru){push @aisatu_data,"$k_id<>$name<>$hatugen<>$ima_time<>\n";}
	
	open(IN,"> $aisatu_datfile") || &error("Open Error : $aisatu_detfile");
	eval{ flock (IN, 2); };
	print IN @aisatu_data;
	close(IN);
	
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
	$in{'mode'} = "login_view";
	&login_view;
	
	exit;
}

###持ち物チェックサブルーチン
sub motimono_kensa {
if(!$k_id){$k_id=$in{'k_id'};}
	$monokiroku_file="./member/$k_id/mono.cgi";
#	if (! -e $monokiroku_file){open (OUT,">$monokiroku_file") || &error("自分の購入物ファイルを作成できません");}
#	close(OUT);
	open(OUT,"< $monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); };
	@my_kounyuu_list =<OUT>;
	close(OUT);
	$kensa_flag=0;
	foreach $one_kounyuu_item (@my_kounyuu_list){
		&syouhin_sprit ($one_kounyuu_item);
		if ($syo_syubetu eq  "ギフト"){next;} #koko2006/11/15
		if ($syo_taikyuu <= 0){next;}
		foreach $check_item (@_){
			if ($check_item eq "$syo_hinmoku"){$kensa_flag=1;last;}
		}
	}
}

##### プレゼント koko 200/05/09 ######
sub kifu{
	open(IN,"< $logfile") || &error("Open Error : $logfile");
	eval{ flock (IN, 2); };
	@aite_erabi = <IN>;
	close(IN);
	$randed= int (rand($#aite_erabi+1));#koko 注意
	$aite_erabi=splice(@aite_erabi,$randed,1);
	($aite_id) = split(/<>/,$aite_erabi);
	if ($aite_id eq "$k_id"){
		$happend_ivent .= "<div class=purasu>●なんかしらんけどＫポイントが５Ｐあがったで。</div>";
		return;
	}

	&lock;	
	&openAitelog ($aite_id);

	$money -= $okane;
	$aite_bank += $okane;
	$kpoint += 3;
	
	&aite_temp_routin;
	open(OUT,">$aite_log_file") || &error("$aite_log_fileが開けません");
	eval{ flock (OUT, 2); };
	print OUT $aite_k_temp;
	close(OUT);
#ver.1.40ここまで
	&aite_kityou_syori("プレゼント←$name","",$okane,$aite_bank,"普",$aite_id,"lock_off");
	&unlock;

	$happend_ivent .= "<div class=mainasu>●$aite_nameさんに$okane円プレゼントした。</div><div class=purasu>●Ｋポイントが５Ｐあがりました。</div>";

}
#kokoend
##### 悪魔の笛 koko 200/05/09 ######
sub kifu2{
	open(IN,"< $logfile") || &error("Open Error : $logfile");
	eval{ flock (IN, 2); };
	@aite_erabi = <IN>;
	close(IN);
	$randed= int (rand($#aite_erabi+1));#koko 注意
	$aite_erabi=splice(@aite_erabi,$randed,1);
	($aite_id) = split(/<>/,$aite_erabi);
	if ($aite_id eq "$k_id"){
		$happend_ivent .= "<div class=mainasu>●なんかしらんけどＫポイントが５Ｐさがったで。</div>";
		return;
	}

	&lock;	
	&openAitelog ($aite_id);

	$money += $okane;
	$aite_bank -= $okane;
	$kpoint -= 3;
	
	&aite_temp_routin;
	open(OUT,">$aite_log_file") || &error("$aite_log_fileが開けません");
	eval{ flock (OUT, 2); };
	print OUT $aite_k_temp;
	close(OUT);
#ver.1.40ここまで
	&aite_kityou_syori("悪魔の笛で強奪←$name","",$okane,$aite_bank,"普",$aite_id,"lock_off");
	&unlock;

	$happend_ivent .= "<div class=purasu>●悪魔の笛を吹いて、$aite_nameのお金$okane円奪いました。</div><div class=mainasu>●Ｋポイントが５Ｐさがりました。</div>";

}
#kokoend
##### 天使の笛 koko 200/05/09 ######
sub kifu3{
	open(IN,"< $logfile") || &error("Open Error : $logfile");
	eval{ flock (IN, 2); };
	@aite_erabi = <IN>;
	close(IN);
	$randed= int (rand($#aite_erabi+1));#koko 注意
	$aite_erabi=splice(@aite_erabi,$randed,1);
	($aite_id) = split(/<>/,$aite_erabi);
	if ($aite_id eq "$k_id"){
		$happend_ivent .= "<div class=purasu>●なんかしらんけどＫポイントが５Ｐあがったで。</div>";
		return;
	}

	&lock;	
	&openAitelog ($aite_id);

	$money -= $okane;
	$aite_bank += $okane;
	$kpoint += 3;
	
	&aite_temp_routin;
	open(OUT,">$aite_log_file") || &error("$aite_log_fileが開けません");
	eval{ flock (OUT, 2); };
	print OUT $aite_k_temp;
	close(OUT);
#ver.1.40ここまで
	&aite_kityou_syori("天使の笛でプレゼント→$name",$okane,"",$aite_bank,"普",$aite_id,"lock_off");
	&unlock;

	$happend_ivent .= "<div class=mainasu>●天使の笛を吹いて、善意で$aite_nameにお金$okane円あげました。</div><div class=purasu>●Ｋポイントが５Ｐあがりました。</div>";

}
#kokoend
###持ち物チェックサブルーチンイベント用　koko2005/09/05
sub motimono_kensa_ev {		#ver.1.40
if(!$k_id){&error("k_idがないよ");}
	$monokiroku_file="./member/$k_id/mono.cgi";
#	if (! -e $monokiroku_file){open (OUT,">$monokiroku_file") || &error("自分の購入物ファイルを作成できません");}
#	close(OUT);
	open(OUT,"< $monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); };
	@my_kounyuu_list =<OUT>;
	close(OUT);
	$kensa_flag=0;
	@new_myitem_hairetu = (); #koko2006/06/05
	foreach $one_kounyuu_item (@my_kounyuu_list){
		&syouhin_sprit ($one_kounyuu_item);
		if ($syo_taikyuu <= 0){
				if($syo_hinmoku ne "武器" and $syo_hinmoku ne "防具" and $syo_hinmoku ne "魔法" and $syo_hinmoku ne "御守"){next;}
		}
		foreach $check_item (@_){
			if ($check_item eq "$syo_hinmoku" && $kensa_flag == 0 &&$syo_syubetu ne "ギフト"){
				$kensa_flag=1;
				$syo_taikyuu--; #koko2005/09/04
				if ($syo_taikyuu < 0){
					$dsp_syo_taikyuu = 0;
				}else{
					$dsp_syo_taikyuu = $syo_taikyuu;
				}

#				last; #koko2005/09/04
			}
		}
#koko2005/09/04
		if ($syo_taikyuu <= 0){
				if($syo_hinmoku ne "武器" and $syo_hinmoku ne "防具" and $syo_hinmoku ne "魔法" and $syo_hinmoku ne "御守"){next;}
		  }
		&syouhin_temp;
		push (@new_myitem_hairetu,$syo_temp);
	}	#foreachの閉じ

	#ログ更新
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
			
	#自分の所有物ファイルを更新
	&lock;
	open(OUT,">$monokiroku_file") || &error("Write Error : $monokiroku_file");
	eval{ flock (OUT, 2); };
	print OUT @new_myitem_hairetu;
	close(OUT);	
#koko2006/11/27
	$loop_count = 0;
	while ($loop_count <= 10){
		for (0..50){$i=0;}#koko2007/06/19
		@f_stat_b = stat($monokiroku_file);
		$size_f = $f_stat_b[7];
		if ($size_f == 0 && @new_myitem_hairetu ne ""){
		#	sleep(1);#2006/11/27#koko2007/02/02
			open (OUT, "> $monokiroku_file") or &error("エラー・ファイルが開けません $monokiroku_file");
			eval{ flock (OUT, 2); };
			print OUT @new_myitem_hairetu;
			close (OUT);
		}else{
			last;
		}
		$loop_count++;
	}
#kokoend
	&unlock;
#kokoend
}

#指定のものをいくつか持っているか調べて一個減らす。2007/04/09 見直し
sub motimono_kensa_ev2 {
	@kensa_itm = @_;
	@kensa_itm0 = @kensa_itm;
	if(!$k_id){&error("mono.cgi エラー event3")} #koko2007/11/18
	$monokiroku_file="./member/$k_id/mono.cgi";
#	if (! -e $monokiroku_file){open (OUT,">$monokiroku_file") || &error("自分の購入物ファイルを作成できません");}
#	close(OUT);
	open(OUT,"< $monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); };
	@my_kounyuu_list =<OUT>;
	close(OUT);
	$kensa_flag=0;
	$i = 0;
	$mae = "";
	@kensa_itm1 = (); #koko2007/07/16
	@kensa_itm0_0 = (@kensa_itm0); #koko2007/07/16 重要修正
	foreach $one_kounyuu_item (@my_kounyuu_list){
		&syouhin_sprit ($one_kounyuu_item);
		if ($syo_syubetu eq  "ギフト"){next;} #koko2006/11/15
		if ($syo_taikyuu <= 0){
				if($syo_hinmoku ne "武器" and $syo_hinmoku ne "防具" and $syo_hinmoku ne "魔法" and $syo_hinmoku ne "御守"){next;}
		  }
		$i = 0;
		foreach $itchi(@kensa_itm0_0){
			if ($itchi eq $syo_hinmoku && $syo_hinmoku ne $mae){
				$motimono_ittci++;
				$mae = $syo_hinmoku;
				push @kensa_itm1 ,$itchi;
				substr @kensa_itm0,$i,1;
				last;
			}
			$i++;

		}
	}
	if ($motimono_ittci < $#kensa_itm + 1){return;}
	$kensa_flag = 1;
	$i = 0;
	$mae = "";
	@new_myitem_hairetu = (); #koko2007/06/05
	foreach $one_kounyuu_item (@my_kounyuu_list){
		&syouhin_sprit ($one_kounyuu_item);
		if (!($syo_taikyuu <= 0)){
			$i = 0;
			@kensa_itm2 = (@kensa_itm1);
			foreach $itchi(@kensa_itm1){
				if ($itchi eq $syo_hinmoku && $syo_syubetu ne "ギフト" && $syo_hinmoku ne $mae){
					$syo_taikyuu--;
					@atta = (@atta,$syo_hinmoku);
					substr @kensa_itm2,$i,1;
					$mae = $syo_hinmoku;
				#	$dsp_syo_taikyuu .= "$syo_hinmoku $syo_taikyuu<br>;
					last;
				}
				$i++;
			}
			@kensa_itm1 = (@kensa_itm2);
		}
	#	if ($syo_taikyuu <= 0){next;}
		&syouhin_temp;
		push (@new_myitem_hairetu,$syo_temp);
	}	#foreachの閉じ
#	練金アイテムへの拡張 
#	$renkin_item = "練金アイテム<>満腹餃子<>0<>0<>0<>0<>0<>0<>0<>食料品<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>1<>回<>0<>0<>3000<><>0<>0<>練金で作られました。<><><><>\n"; #数を増やすことが出来ない。
#	push (@new_myitem_hairetu,$renkin_item);

	#ログ更新
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
			
	#自分の所有物ファイルを更新
	open(OUT,">$monokiroku_file") || &error("Write Error : $monokiroku_file");
	eval{ flock (OUT, 2); };
	print OUT @new_myitem_hairetu;
	close(OUT);	
}

###### クーポン処理 ######
sub coupon_get{
	$coupointo = $_[0];
if(!$k_id){&error("k_idがないよ");}
	$monokiroku_file="./member/$k_id/mono.cgi";
#	if (! -e $monokiroku_file){open (OUT,">$monokiroku_file") || &error("自分の購入物ファイルを作成できません");}
#	close(OUT);
	open(OUT,"< $monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); };
	@my_kounyuu_list =<OUT>;
	close(OUT);

	$kensa_flag=0;
	@new_myitem_hairetu = (); #koko2006/06/05
	foreach $one_kounyuu_item (@my_kounyuu_list){
		&syouhin_sprit ($one_kounyuu_item);
		if ($syo_syubetu eq 'ギフト' && $syo_hinmoku eq 'クーポン'){
			$syo_taikyuu += $coupointo;
			$kensa_flag = 1;
		}
		&syouhin_temp;
		push @new_myitem_hairetu,$syo_temp;
	}
	if ($kensa_flag != 1){
		open(OUT,"< ./dat_dir/prezento.cgi") || &error("プレゼントリストが開けません");
		eval{ flock (OUT, 2); };
		@prezento =<OUT>;
		close(OUT);
		foreach (@prezento){
			&syouhin_sprit ($_);
			if ($syo_hinmoku eq 'クーポン'){
				$kensa_flag = 1;
				$syo_syubetu = 'ギフト';
				$syo_taikyuu = $coupointo;
				$syo_kounyuubi = time;
				$tanka = 0;
				&syouhin_temp;
				push @new_myitem_hairetu,$syo_temp;
				last;
			}
		}
		if ($kensa_flag != 1){&error("クーポンの取り扱いありません");}
	}
	#自分の所有物ファイルを更新
	open(OUT,">$monokiroku_file") || &error("Write Error : $monokiroku_file");
	eval{ flock (OUT, 2); };
	print OUT @new_myitem_hairetu;
	close(OUT);	
}
# イベントでのアイテムゲット　制限無し　区分は元のままでもよい。
sub get_itm{
	$getitm = $_[0];
#	0=英文解釈教室 1=成り上がり 2=おばあちゃんの知恵袋 今はこれだけ　持ち物オーバーでも増えていきます。規制は入っていません。
	@plazentitm =(
'ゲットアイテム<>英文解釈教室<>0<>0<>0<>0<>5<>0<>0<>無<>0<>0<>0<>0<>0<>0<>0<>1000<>0<>0<>0<>3<>回<>30<>5<>0<><><>10<><>0<>0<>0<>\n'
,'ゲットアイテム<>成り上がり<>0<>0<>0<>0<>0<>6<>0<>無<>0<>0<>0<>0<>0<>0<>0<>400<>0<>0<>0<>3<>回<>30<>15<>0<><><>3<><>0<>0<>0<>\n'
,'ゲットアイテム<>おばあちゃんの知恵袋<>3<>3<>3<>3<>3<>3<>3<>無<>0<>0<>0<>0<>0<>0<>0<>2000<>0<>0<>0<>2<>回<>30<>5<>0<><><>10<><>0<>0<>0<>\n'
);
	if ($#plazentitm < $getitm){&error("その品物は準備されていません。");}

if(!$k_id){&error("k_idがないよ");}
	$monokiroku_file="./member/$k_id/mono.cgi";
#	if (! -e $monokiroku_file){open (OUT,">$monokiroku_file") || &error("自分の購入物ファイルを作成できません");}
#	close(OUT);
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

# イベントでのアイテムゲット　制限無し　区分は元のままでもよい。
sub get_itm2{
	$getitm = $_[0];
#	0=英文解釈教室 1=成り上がり 2=おばあちゃんの知恵袋 今はこれだけ　持ち物オーバーでも増えていきます。規制は入っていません。
	@plazentitm =(
'ゲットアイテム<>悪魔の笛<>0<>0<>0<>0<>0<>0<>0<>無<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>5<>回<>10<>5<>0<><><>0<>何が起こるのだろう？<>0<>0<>0<>\n'
,'ゲットアイテム<>天使の笛<>0<>0<>0<>0<>0<>0<>0<>無<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>5<>回<>10<>5<>0<><><>0<>何が起こるのだろう？<>0<>0<>0<>\n'
,'ゲットアイテム<>４次元福袋<>1<>1<>1<>1<>1<>1<>1<>無<>1<>1<>1<>1<>1<>1<>1<>10000<>1<>1<>5<>10<>回<>30<>0<>0<><><><><>クリスマスプレゼントです<><><>\n'
,'ゲットアイテム<>等身大サンタさん人形<>1<>1<>1<>1<>1<>1<>1<>無<>1<>1<>1<>1<>1<>1<>1<>10000<>1<>1<>5<>10<>回<>30<>0<>0<><><><><>クリスマスプレゼントです<><><>\n'
,'ゲットアイテム<>クリスマスケーキ１日分<>1<>1<>1<>1<>1<>1<>1<>ウエイトアップ,1,食料品<>1<>1<>1<>1<>1<>1<>1<>10000<>1<>1<>2<>1<>回<>30<>0<>100<><><><><>クリスマスプレゼントです<><><>\n'
,'ゲットアイテム<>トナカイの肉１匹分<>0<>0<>0<>0<>0<>0<>0<>無<>2<>2<>2<>2<>2<>2<>2<>1000<>2<>2<>2<>1<>回<>30<>0<>10<><><><><>クリスマスプレゼントです<><><>\n'
,'ゲットアイテム<>巨大クリスマスツリー<>1<>1<>1<>1<>1<>1<>1<>無<>1<>1<>1<>1<>1<>1<>1<>10000<>1<>1<>50<>1<>回<>1<>0<>0<><><><>クリスマスプレゼントです<><><><>\n'

);
	if ($#plazentitm < $getitm){&error("その品物は準備されていません。");}

if(!$k_id){&error("k_idがないよ");}
	$monokiroku_file="./member/$k_id/mono.cgi";
#	if (! -e $monokiroku_file){open (OUT,">$monokiroku_file") || &error("自分の購入物ファイルを作成できません");}
#	close(OUT);
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
###### イベント記録 #####
sub event_kiroku{
	$evento_kirokosuu = 150; #イベントの記録数
	&time_get;
	open(IN,"< $event_fail") || &error("$event_failが開けません。");
	eval{ flock (IN, 1); };
	@town_event = <IN>;
	close(IN);
	$happend_ivent2 = $_[1];
	$happend_ivent2 =~ s/\n//g;
	$event_kizi = "$date2<>$_[0]<>$happend_ivent2<>\n";
	unshift (@town_event,$event_kizi);
	if($#town_event+1 >= $evento_kirokosuu){$#town_event = $evento_kirokosuu-1;}
	open(OUT,">$event_fail") || &error("$event_failに書き込めません");
	eval{ flock (OUT, 2); };
	print OUT @town_event;
	close(OUT);
}

1;
