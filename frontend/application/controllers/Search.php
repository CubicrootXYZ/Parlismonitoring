<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Search extends CI_Controller {

	/**
	 * Index Page for this controller.
	 *
	 * Maps to the following URL
	 * 		http://example.com/index.php/welcome
	 *	- or -
	 * 		http://example.com/index.php/welcome/index
	 *	- or -
	 * Since this controller is set as the default controller in
	 * config/routes.php, it's displayed at http://example.com/
	 *
	 * So any other public methods not prefixed with an underscore will
	 * map to /index.php/welcome/<method_name>
	 * @see https://codeigniter.com/user_guide/general/urls.html
	 */
	public function index()
	{
		$this->load->helper('url');
		$this->load->model('searching');

        $data['title'] = 'Suche';
        if ($_SERVER['REQUEST_METHOD'] === 'GET' ) {
			$search = $_GET;
		} else {
			$search = '';
		}

        $data['content'] = $this->searching->getSearch($search);
        $data['authors'] = $this->searching->getAuthors();
		
		$this->load->view('templates/header', $data);
		$this->load->view('search');
		$this->load->view('templates/footer', $data);
        
	}

	
}
