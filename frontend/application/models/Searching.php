<?php
class Searching extends CI_Model {

        public function __construct()
        {
            
        }

        public function getSearch($data) {
            $ret = [];


            $append = "";

            if (sizeof($data) < 1) {
                return $ret;
            } else {
                foreach ($data as $key => $value) {
                    $append .= urlencode($key)."=".urlencode($value)."&";
                }
                $append = substr($append,0,-1);
            }

           

            
            if(isset($data['experimental']) && $data['experimental'] == "true") {
                try {
                    $content = json_decode(file_get_contents(APIURL."searchfilesexperimental?".$append), true);
                } catch (Exception $e) {
                    $ret = [];
                    return $ret;
                } 
            } else {
                try {
                    print(APIURL."searchfiles?".$append);
                    $content = json_decode(file_get_contents(APIURL."searchfiles?".$append), true);
                } catch (Exception $e) {
                    $ret = [];
                    return $ret;
                } 
            }

            if ($content['status'] != 'success') {
                $ret = [];
                return $ret;
            }

            return $content['data'];
        }

        public function getAuthors() {
            try {
                $content = json_decode(file_get_contents(APIURL."authors"), true);
            } catch (Exception $e) {
                $ret = [];
                return $ret;
            } 

            if ($content['status'] != 'success') {
                $ret = [];
                return $ret;
            }

            return $content['data'];
        }

}




