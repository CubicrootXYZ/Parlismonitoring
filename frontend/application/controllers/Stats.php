<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Stats extends CI_Controller {

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
		$this->load->model('statistics');

		$data['title'] = 'Home';

		$data['wordclouds'] = $this->statistics->getWordClouds();
		$data['wordcloud_all'] = $this->statistics->getWordCloud();


		
		$this->load->view('templates/header', $data);
		$this->load->view('welcome_message');
		$this->load->view('templates/footer', $data);
        
	}

	public function trends()
	{
		$this->load->helper('url');
		$this->load->model('statistics');

		if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['search'])) {
			$search = $_GET['search'];
		} else {
			$search = '';
		}

		if (isset($_GET['daily']) && $_GET['daily'] == 'true') {
			$data['values'] = $this->statistics->getWordByDay($search);
		} else {
			$data['values'] = $this->statistics->getWordByMonth($search);
		}

		$data['title'] = 'Trends';

		

		
		$this->load->view('templates/header', $data);
		$this->load->view('trends');
		$this->load->view('templates/footer', $data);
        
	}

	public function trendsbymonth()
	{
		$this->load->helper('url');
		$this->load->model('statistics');

		if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['search'])) {
			$search = $_GET['search'];
		} else {
			$search = '';
		}

		$data['title'] = 'Trends (Monate)';

		$data['values'] = $this->statistics->getWordByMonth($search);

		
		$this->load->view('templates/header', $data);
		$this->load->view('trends');
		$this->load->view('templates/footer', $data);
        
	}

	public function trendsbyparty()
	{
		$this->load->helper('url');
		$this->load->model('statistics');

		if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['search'])) {
			$search = $_GET['search'];
		} else {
			$search = '';
		}

		if (isset($_GET['daily']) && $_GET['daily'] == 'true') {
			$data['values'] = $this->statistics->getWordByDayAndAuthor($search);
		} else {
			$data['values'] = $this->statistics->getWordByMonthAndAuthor($search);
		}

		$data['title'] = 'Trends nach Partei';

		
		$this->load->view('templates/header', $data);
		$this->load->view('trendsbyparty');
		$this->load->view('templates/footer', $data);
        
	}

	public function trendsbymonthandparty()
	{
		$this->load->helper('url');
		$this->load->model('statistics');

		if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['search'])) {
			$search = $_GET['search'];
		} else {
			$search = '';
		}

		$data['title'] = 'Trends nach Partei (Monat)';

		$data['values'] = $this->statistics->getWordByMonthAndAuthor($search);

		
		$this->load->view('templates/header', $data);
		$this->load->view('trendsbyparty');
		$this->load->view('templates/footer', $data);
        
	}
}
