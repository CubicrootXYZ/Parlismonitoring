<?php
class Statistics extends CI_Model {

        public function __construct()
        {
            
        }

        public function getWordClouds() {
            $ret = [];
            try {
                $content = json_decode(file_get_contents(APIURL."wordclouds"), true);

            } catch (Exception $e) {
                $ret[0]['data'] = '[{"tag": "404 API down", "weight": 100}]';
                $ret[0]['name'] = '-';
                return $ret;
            }

            if ($content['status'] != 'success') {
                $ret[0]['data'] = '[{"tag": "404 API down", "weight": 100}]';
                $ret[0]['name'] = '-';
                return $ret;
            }

            foreach ($content['data'] as $name => $entry) {
                $val['name'] = $name;
                $val['data'] = '[';
                $i = 0;

                if ($name == "LRG") {
                    $val['name'] = 'LRG (Landesregierung)';
                }

                if ($name == "AfD") {
                    $val['color1'] = '#009cdf';
                    $val['color2'] = '#b3e7fd';
                    $val['color_bg'] = '#ffffff';
                } else if ($name == "SPD") {
                    $val['color1'] = '#f10009';
                    $val['color2'] = '#ff9a9e';
                    $val['color_bg'] = '#ffffff';
                } else if ($name == "FDP/DVP") {
                    $val['color1'] = '#ffd600';
                    $val['color2'] = '#fdeb8c';
                    $val['color_bg'] = '#ffffff';
                } else if ($name == "GRÜNE") {
                    $val['color1'] = '#01760b';
                    $val['color2'] = '#94e29a';
                    $val['color_bg'] = '#ffffff';
                } else {
                    $val['color1'] = '#000000';
                    $val['color2'] = '#c7c7c7';
                    $val['color_bg'] = '#ffffff';
                }

                foreach ($entry as $word => $amount) {
                    if ($i < MAXAMOUNTWORDCLOUDS) {
                        $val['data'] .= '{"tag": "'.$word.'", "weight": '.$amount.'},';
                    }
                    
                    $i += 1;
                }

                $val['data'] = substr($val['data'], 0, -1);
                $val['data'] .= "]";
                array_push($ret, $val);
            }

            return $ret;
        }

        public function getWordCloud() {
            $ret = "[";
            try {
                $content = json_decode(file_get_contents(APIURL."wordcloud"), true);

            } catch (Exception $e) {
                $ret .= '{"tag": "404 API down", "weight": 100}]';
                return $ret;
            }

            if ($content['status'] != 'success') {
                $ret .= '{"tag": "404 API down", "weight": 100}]';
                return $ret;
            }

            foreach ($content['data'] as $entry) {
                
                $ret .= '{"tag": "'.$entry['word'].'", "weight": '.$entry["counter"].'},';
            }

            $ret = substr($ret, 0, -1);
            $ret .= "]";

            return $ret;
            
        }

        public function getWordByDay($search) {

            $final = [];
            $search = str_replace(" ", "", $search);
            $search_words = explode(",", $search);
            $colors = ['#ff8800', '#0a7fdc', '#018800', '#000000', '#b00101', '#d6d600'];
            $searchwords = [];

            $values = [];
            $i = 0;
            $j = 0;
            $ret= '[';

            if (strlen($search) == 0) {
                try {
                    $content = json_decode(file_get_contents(APIURL."wordcloud"), true);
    
                } catch (Exception $e) {
                    $ret .= '';
                    return $ret;
                }
    
                if ($content['status'] != 'success') {
                    $ret .= '';
                    return $ret;
                }

                while ($j < 5) {
                    if (isset($content['data'][$j]['word'])) {
                        $search_words[$j] = $content['data'][$j]['word'];
                    }                    
                    $j += 1;
                }
    
            }

            foreach ($search_words as $search_word) {
                array_push($searchwords, $search_word);


                
                if ($i <= 5 && strlen($search_word) > 0) {
                    try {
           
                        $content = json_decode(file_get_contents(APIURL."wordbyday/".urlencode($search_word)), true);
        
                    } catch (Exception $e) {
                        $ret['data'] = '';
                        $ret['amount'] = -1;
                        return $ret;
                    }
                    if ($content['status'] != 'success') {
                        $ret['data'] = '';
                        $ret['amount'] = -1;
                        return $ret;
                    }
        
                    ksort($content['data']);
    
                    foreach ($content['data'] as $date => $count) {
                        $date_ = explode("-", $date)[0]."-".explode("-", $date)[1]."-".explode("-", $date)[2];
                        $values[$date_][$i] = $count;
                    }
                }
                

                $i += 1;
            
            }

            ksort($values);

            foreach ($values as $date => $value) {
                $ret .= '{"date": "'.$date.'"';
                    
                    $i2 = $i-1;
                    while ($i2 >= 0) {
                        if (isset($value[$i2])) {
                            $ret .= ', "value'.$i2.'": '.$value[$i2];
                        } else {
                            $ret .= ', "value'.$i2.'": 0';
                        }
                        $i2 -= 1;
                    }

                
                $ret .= '},';
            }

            if (strlen($ret) > 1) {
                $ret = substr($ret, 0, -1);
            }
            
            $ret .= "]";

            $return['data'] = $ret;
            $return['amount'] = $i;
            $return['color'] = $colors;
            $return['searchwords'] = $searchwords;
            return $return;
        }

        public function getWordByDayAndAuthor($search) {
            $final = '';
            $search = str_replace(" ", "", $search);
            $colors = ['#ff8800', '#0a7fdc', '#018800', '#000000', '#b00101', '#d6d600'];
            $values = [];
            $i = 0;
            $ret= [];


                
                if (strlen($search) > 0) {
                    try {
                        $content = json_decode(file_get_contents(APIURL."wordbydayandauthor/".urlencode($search)), true);
        
                    } catch (Exception $e) {
                        $ret['data'] = '';
                        $ret['amount'] = -1;
                        return $ret;
                    }
                    if ($content['status'] != 'success') {
                        $ret['data'] = '';
                        $ret['amount'] = -1;
                        return $ret;
                    }
        
                    ksort($content['data']);

                    foreach ($content['data'] as $author => $data) {
                        foreach ($data as $date => $count) {
                            $date_ = explode("-", $date)[0]."-".explode("-", $date)[1]."-".explode("-", $date)[2];
                            $values[$date_][$author] = $count;
                        }

                            if ($author == "AfD") {
                                $return['colors'][$author] = '#009cdf';
                            } else if ($author == "SPD") {
                                $return['colors'][$author] = '#f10009';
                            } else if ($author == "FDP/DVP") {
                                $return['colors'][$author] = '#ffd600';
                            } else if ($author == "GRÜNE") {
                                $return['colors'][$author] = '#01760b';
                            } else if ($author == "CDU") {
                                $return['colors'][$author] = '#000000';
                            } else if ($author == "LRG" || $author == "Ausschüsse") {
                            } else {
                                $return['colors'][$author] = '#dbdbdb';
                            }
                    }

    
                }
            else {
                $ret['data'] = '';
                $ret['amount'] = -1;
                return $ret;
            }

            $final = "[";

            ksort($values);

            foreach ($values as $date => $data) {
                $final .= '{"date": "'.$date.'", ';
                    foreach($return['colors'] as $auth => $color) {
                        if (isset($data[$auth])) {
                            $final .= '"'.$auth.'": "'.$data[$auth].'",';
                        } else {
                            $final .= '"'.$auth.'": "0",';
                        }
                    }

                    
                $final = substr($final,0,-1);
                $final .= "},";
            }
            $final = substr($final,0,-1);
            $final .= "]";
                

            

            $return['data'] = $final;
            $return['search'] = $search;
            return $return;
        }

        public function getWordByMonthAndAuthor($search) {
            $final = '';
            $search = str_replace(" ", "", $search);
            $colors = ['#ff8800', '#0a7fdc', '#018800', '#000000', '#b00101', '#d6d600'];
            $values = [];
            $i = 0;
            $ret= [];


                
                if (strlen($search) > 0) {
                    try {
                        $content = json_decode(file_get_contents(APIURL."wordbymonthandauthor/".urlencode($search)), true);
        
                    } catch (Exception $e) {
                        $ret['data'] = '';
                        $ret['amount'] = -1;
                        return $ret;
                    }
                    if ($content['status'] != 'success') {
                        $ret['data'] = '';
                        $ret['amount'] = -1;
                        return $ret;
                    }
        
                    ksort($content['data']);

                    foreach ($content['data'] as $author => $data) {
                        foreach ($data as $date => $count) {
                            $date_ = explode(".", $date)[1]."-".explode(".", $date)[0];
                            $values[$date_][$author] = $count;
                        }

                            if ($author == "AfD") {
                                $return['colors'][$author] = '#009cdf';
                            } else if ($author == "SPD") {
                                $return['colors'][$author] = '#f10009';
                            } else if ($author == "FDP/DVP") {
                                $return['colors'][$author] = '#ffd600';
                            } else if ($author == "GRÜNE") {
                                $return['colors'][$author] = '#01760b';
                            } else if ($author == "CDU") {
                                $return['colors'][$author] = '#000000';
                            } else if ($author == "LRG" || $author == "Ausschüsse") {
                            } else {
                                $return['colors'][$author] = '#dbdbdb';
                            }
                    }

    
                }
            else {
                $ret['data'] = '';
                $ret['amount'] = -1;
                return $ret;
            }

            $final = "[";

            ksort($values);

            foreach ($values as $date => $data) {
                $final .= '{"date": "'.$date.'", ';
                    foreach($return['colors'] as $auth => $color) {
                        if (isset($data[$auth])) {
                            $final .= '"'.$auth.'": "'.$data[$auth].'",';
                        } else {
                            $final .= '"'.$auth.'": "0",';
                        }
                    }

                    
                $final = substr($final,0,-1);
                $final .= "},";
            }
            $final = substr($final,0,-1);
            $final .= "]";
                

            

            $return['data'] = $final;
            $return['search'] = $search;
            return $return;
        }

        public function getWordByMonth($search) {

            $final = [];
            $search = str_replace(" ", "", $search);
            $search_words = explode(",", $search);
            $colors = ['#ff8800', '#0a7fdc', '#018800', '#000000', '#b00101', '#d6d600'];
            $searchwords = [];

            $values = [];
            $i = 0;
            $j = 0;
            $ret= '[';

            if (strlen($search) == 0) {
                try {
                    $content = json_decode(file_get_contents(APIURL."wordcloud"), true);
    
                } catch (Exception $e) {
                    $ret .= '';
                    return $ret;
                }
    
                if ($content['status'] != 'success') {
                    $ret .= '';
                    return $ret;
                }

                while ($j < 5) {
                    if (isset($content['data'][$j]['word'])) {
                        $search_words[$j] = $content['data'][$j]['word'];
                    }                    
                    $j += 1;
                }
    
            }

            foreach ($search_words as $search_word) {
                array_push($searchwords, $search_word);


                
                if ($i <= 5 && strlen($search_word) > 0) {
                    try {
           
                        $content = json_decode(file_get_contents(APIURL."wordbymonth/".urlencode($search_word)), true);
        
                    } catch (Exception $e) {
                        $ret['data'] = '';
                        $ret['amount'] = -1;
                        return $ret;
                    }
                    if ($content['status'] != 'success') {
                        $ret['data'] = '';
                        $ret['amount'] = -1;
                        return $ret;
                    }
        
                    ksort($content['data']);
    
                    foreach ($content['data'] as $date => $count) {
                        $date_ = explode(".", $date)[1]."-".explode(".", $date)[0];
                        $values[$date_][$i] = $count;
                    }
                }
                

                $i += 1;
            
            }

            ksort($values);

            foreach ($values as $date => $value) {
                $ret .= '{"date": "'.$date.'"';
                    
                    $i2 = $i-1;
                    while ($i2 >= 0) {
                        if (isset($value[$i2])) {
                            $ret .= ', "value'.$i2.'": '.$value[$i2];
                        } else {
                            $ret .= ', "value'.$i2.'": 0';
                        }
                        $i2 -= 1;
                    }

                
                $ret .= '},';
            }

            if (strlen($ret) > 1) {
                $ret = substr($ret, 0, -1);
            }
            
            $ret .= "]";

            $return['data'] = $ret;
            $return['amount'] = $i;
            $return['color'] = $colors;
            $return['searchwords'] = $searchwords;
            return $return;
        }
}




