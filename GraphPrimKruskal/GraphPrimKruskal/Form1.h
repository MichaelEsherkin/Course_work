#pragma once

namespace GraphPrimKruskal {

	using namespace System;
	using namespace System::ComponentModel;
	using namespace System::Collections::Generic;
	using namespace System::Windows::Forms;
	using namespace System::Data;
	using namespace System::Drawing;

	public ref class Form1 : public System::Windows::Forms::Form {
		// ��������� ��� ������ �����
		ref struct Vertex {
			int id; // ������ �������
			int x; // ���������� �� �
			int y; // ���������� �� �
		};

		// ��������� ��� ���� �����
		ref struct Edge {
			int v1; // ������ �������
			int v2; // ������ �������
			double w; // ��� �����
		};

		const int r = 16; // ������ ������
		const int INF = 1000000; // �������������

		Bitmap ^bitmap; // �������� ��� ���������
		Graphics ^g; // �������

		List<Vertex^> ^vertices; // �������
		List<Edge^> ^edges; // ����
		Vertex ^start = nullptr; // ��������� ������� �����



	private: System::Windows::Forms::StatusStrip^  statusStrip1;
	private: System::Windows::Forms::ToolStripStatusLabel^  toolStripStatusLabel1;
	private: System::Windows::Forms::DataGridViewTextBoxColumn^  v1;
	private: System::Windows::Forms::DataGridViewTextBoxColumn^  v2;
	private: System::Windows::Forms::DataGridViewTextBoxColumn^  length;
	private: System::Windows::Forms::RichTextBox^  ResBox;




		Pen ^edgePen; // ����� ��� ��������� ����

	public:
		Form1(void) {
			InitializeComponent();

			vertices = gcnew List<Vertex^>(); // ������ ������ ������
			edges = gcnew List<Edge^>(); // ������ ������ ����

			edgePen = Pens::Black; // ����� ��� ����

			bitmap = gcnew Bitmap(Canvas->Width, Canvas->Height); // ������ ��������
			g = Graphics::FromImage(bitmap); // ������ �������
			g->Clear(Color::White); // ������� ��������

			Canvas->Image = bitmap; // ���������� ��������
		}

	protected:
		// ��������� ������
		void DrawVertices() {
			System::Drawing::Font ^font = gcnew System::Drawing::Font(Font->Name, 10);

			for (int i = 0; i < vertices->Count; i++) {
				int x = vertices[i]->x;
				int y = vertices[i]->y;
				String ^name = vertices[i]->id + 1 + "";

				SizeF size = g->MeasureString(name, font); // �������� ������
				g->FillEllipse(start != nullptr && start->Equals(vertices[i]) ? Brushes::LightGreen : Brushes::Orange, x - r, y - r, 2 * r, 2 * r);
				g->DrawString(name, font, Brushes::White, x - size.Width / 2, y - size.Height / 2); // ������ �����
			}
		}

		// ��������� ����
		void DrawEdges() {
			System::Drawing::Font ^font = gcnew System::Drawing::Font(Font->Name, 10);

			for (int i = 0; i < edges->Count; i++) {
				Vertex ^v1 = vertices[edges[i]->v1];
				Vertex ^v2 = vertices[edges[i]->v2];
				String ^w = edges[i]->w + "";

				int x = (v1->x + v2->x) / 2;
				int y = (v1->y + v2->y) / 2;

				g->DrawLine(edgePen, v1->x, v1->y, v2->x, v2->y);
				g->DrawString(w, font, Brushes::Black, x, y);
			}
		}

		// ��������� ��������
		void Draw() {
			g->Clear(Color::White); // ������� ��������

			DrawEdges(); // ������������ ����
			DrawVertices(); // ������������ �������

			Canvas->Image = bitmap; // ��������� ��������

			bool mayTree = vertices->Count > 0;
			PrimItem->Enabled = mayTree;
			KruskalItem->Enabled = mayTree;

			toolStripStatusLabel1->Text = "������: " + (vertices->Count> 0 ? vertices->Count + "" : "���") + ", ����: " + (edges->Count > 0 ? edges->Count + "" : "���");
		}

		// ����� ������� � �����
		int IndexOfVertex(int x, int y, double maxdst) {
			for (int i = 0; i < vertices->Count; i++) {
				double dx = x - vertices[i]->x;
				double dy = y - vertices[i]->y;
				double dst = Math::Sqrt(dx * dx + dy * dy); // ������� ���������� �� ������

				if (dst < maxdst)
					return i; // ���������� ������
			}

			return -1; // �� �����
		}

		// �������� ������� �����
		int HaveEdge(int v1, int v2) {
			for (int i = 0; i < edges->Count; i++) {
				if (edges[i]->v1 == v1 && edges[i]->v2 == v2)
					return i;

				if (edges[i]->v1 == v2 && edges[i]->v2 == v1)
					return i;
			}

			return -1;
		}

		// ������������ �����
		void MakeEdge(int x, int y, int index) {
			if (start == nullptr) {
				start = vertices[index]; // ���������� ��������� �������
				return; // �������
			}

			int v1 = start->id;
			int v2 = vertices[index]->id;

			start = nullptr; // ���������� �����

			// ��������� ���� � ����� ���� � �� ��������� ����, ������� � ��� ��� ����
			if (v1 != v2 && HaveEdge(v1, v2) == -1) {
				Edge ^edge = gcnew Edge(); // ������ ����� �����
				edge->v1 = v1;
				edge->v2 = v2;
				edge->w = 0;

				edges->Add(edge); // ��������� �����
				EdgeGrid->Rows->Add(v1 + 1, v2 + 1, 0);
			}

			Draw(); // ��������� ��������
		}

		// ���������� �������
		void AddVertex(int x, int y) {
			int index = IndexOfVertex(x, y, 2 * r); // ���� � ����� �������
			
			// �� ��������� ������� � ��� �� �����
			if (index != -1) {
				MakeEdge(x, y, index);
				return;
			}

			Vertex ^vertex = gcnew Vertex();
			vertex->x = x;
			vertex->y = y;
			vertex->id = vertices->Count;
			vertices->Add(vertex); // ��������� �������
			Draw(); // �������������� ��������
		}

		// �������� �������
		void RemoveVertex(int x, int y) {
			int index = IndexOfVertex(x, y, r); // �������� ������ �������

			// ���� �� ����� �������
			if (index == -1)
				return; // �� �������

			int v = vertices[index]->id;

			for (int i = edges->Count - 1; i >= 0; i--) {
				int v1 = edges[i]->v1;
				int v2 = edges[i]->v2;

				if (v1 == v || v2 == v) {
					edges->RemoveAt(i);
					EdgeGrid->Rows->RemoveAt(i);
				}
			}

			vertices->RemoveAt(index); // ������� �������

									  // ��������� ������ ������
			for (int i = 0; i < vertices->Count; i++) {
				Vertex ^vertex = vertices[i]; // �������� �������
				vertex->id = i; // ��������� ������ �������
				vertices[i] = vertex; // ��������� �������
			}

			EdgeGrid->Rows->Clear();

			// ��������� ����� �� �����
			for (int i = 0; i < edges->Count; i++) {
				Edge ^edge = edges[i];

				if (edge->v1 > v)
					edge->v1--;

				if (edge->v2 > v)
					edge->v2--;

				edges[i] = edge;
				EdgeGrid->Rows->Add(edge->v1 + 1, edge->v2 + 1, edge->w);
			}

			Draw(); // ������
		}

		// ���� ������ �� ��������
		private: System::Void Canvas_MouseClick(System::Object^  sender, System::Windows::Forms::MouseEventArgs^  e) {
			if (e->Button == System::Windows::Forms::MouseButtons::Left) { // �� ����� ������ ����
				AddVertex(e->X, e->Y); // ��������� �������
			}
			else if (e->Button == System::Windows::Forms::MouseButtons::Right) { // �� ������ ������ ����
				RemoveVertex(e->X, e->Y); // ������� �������
			}
		}

		// ����������� ���� �� ����
		private: System::Void Canvas_MouseMove(System::Object^  sender, System::Windows::Forms::MouseEventArgs^  e) {
			if (start == nullptr) // ���� ��� ��������� �������
				return; // �������

			Draw(); // ������ ������� ���������
			g->DrawLine(Pens::Black, start->x, start->y, e->X, e->Y); // ������ �����
		}

		// ��������� ��������� �������� �������
		private: System::Void EdgeGrid_CellValueChanged(System::Object^  sender, System::Windows::Forms::DataGridViewCellEventArgs^  e) {
			if (e->RowIndex < 0)
				return;

			Edge ^edge = edges[e->RowIndex];
			edge->w = double::Parse(EdgeGrid[2, e->RowIndex]->Value->ToString()); // ��������� ��� ����� �����
			edges[e->RowIndex] = edge;

			Draw(); // �������������� ����
		}

		// ��������� ������� ������� �������� ��� �������� �����
		private: System::Void EdgeGrid_KeyDown(System::Object^  sender, System::Windows::Forms::KeyEventArgs^  e) {
			if (e->KeyCode == Keys::Delete) { // ���� ������ ��������
				if (EdgeGrid->SelectedRows->Count == 0) // ���� ��� ��������� �����
					return; // �������

				int row = EdgeGrid->SelectedRows[0]->Index; // �������� ������

				edges->RemoveAt(row); // ������� �����
				EdgeGrid->Rows->RemoveAt(row); // ������� �� �������
				Draw(); // ��������������
			}
		}

		// ��������� ������������ ������
		void DrawTree(List<int> ^tree, String ^name, int compares) {
			g->Clear(Color::White); // ������� ��������

			DrawEdges(); // ������������ ����

			double len = 0; // ����� ������
			Pen ^pen = gcnew Pen(Color::Blue, 2);

			ResBox->Clear();
			ResBox->AppendText("������: ");

			for (int i = 0; i < tree->Count; i += 2) {
				int v1 = tree[i];
				int v2 = tree[i + 1];

				len += edges[HaveEdge(v1, v2)]->w; // ������� ����� ������
				g->DrawLine(pen, vertices[v1]->x, vertices[v1]->y, vertices[v2]->x, vertices[v2]->y); // ������ ����� ������
				ResBox->AppendText((v1 + 1) + "-" + (v2 + 1) + " ");
			}

			DrawVertices(); // ������������ �������
			Canvas->Image = bitmap; // ��������� ��������            
			toolStripStatusLabel1->Text = "������: " + (vertices->Count> 0 ? vertices->Count + "" : "���") + ", ����: " + (edges->Count > 0 ? edges->Count + "" : "���") + ", ��� ������: " + len;
		}

		// ���������� ������������ ��������� ������
		private: System::Void PrimItem_Click(System::Object^  sender, System::EventArgs^  e) {
			int compares = 0;
			bool *visited = new bool[vertices->Count]; // ������ ������ ��������� ������
			double *min_edge = new double[vertices->Count]; // ������ ����������� ���� ����
			int *end_edge = new int[vertices->Count]; // ������ ������ ������ � �������� ������
			List<int> ^tree = gcnew List<int>();

			for (int i = 0; i < vertices->Count; i++) {
				visited[i] = false;
				min_edge[i] = INF;
				end_edge[i] = -1;
			}

			min_edge[0] = 0; // �������� � ������� �������

			for (int i = 0; i < vertices->Count; i++) {
				int v = -1;

				// ���� ������� � ����������� �����, ������� ��� �� ���� ��������
				for (int j = 0; j < vertices->Count; j++) {
					if (!visited[j] && (v == -1 || min_edge[j] < min_edge[v])) {
						v = j;
						compares++;
					}
				}

				visited[v] = true; // �������� � ��� ����������

								   // ���� �������� ����� � ������� ����������, � ��������� ����� � ������
				if (end_edge[v] != -1) {
					tree->Add(v);
					tree->Add(end_edge[v]);
				}

				// ���������� �� ���� ��������
				for (int to = 0; to < vertices->Count; to++) {
					int edge = HaveEdge(v, to); // �������� ����� �����

												// ���� ��� ���
					if (edge == -1)
						continue; // ��� ������

								  // ����� ���� ��� ����� ������ ������������, �� ��������� ����������� ��� � ���������� ��� �������
					if (edges[edge]->w < min_edge[to]) {
						min_edge[to] = edges[edge]->w;
						end_edge[to] = v;
						compares++;
					}
				}
			}

			DrawTree(tree, "�������� �����", compares);
		}

		// ������ �� ������ ��������
		private: System::Void KruskalItem_Click(System::Object^  sender, System::EventArgs^  e) {
			int compares = 0;

			// ��������� ���� �� ����������� �����
			for (int k = edges->Count / 2; k > 0; k /= 2) {
				for (int i = k; i < edges->Count; i++) {
					int j = i;
					Edge ^tmp = edges[i];

					while (j >= k && tmp->w < edges[j - k]->w) {
						edges[j] = edges[j - k];
						compares++;
						j -= k;
					}

					edges[j] = tmp;
				}
			}

			EdgeGrid->Rows->Clear(); // ������� ������� ����

								   // ��������� ���� � �������
			for (int i = 0; i < edges->Count; i++)
				EdgeGrid->Rows->Add(edges[i]->v1 + 1, edges[i]->v2 + 1, edges[i]->w);

			int *treeId = new int[vertices->Count]; // ������ ������ ��� �������� ������ ������

			// ���������� ��� �������� �������
			for (int i = 0; i < vertices->Count; i++)
				treeId[i] = i;

			List<int> ^tree = gcnew List<int>(); // ������ ��� ������������ ��������� ������

			// ���������� �� ���� �����
			for (int i = 0; i < edges->Count; i++) {
				int v1 = edges[i]->v1;
				int v2 = edges[i]->v2;

				// ���� ������� �� ������ �� ���������, �� ��������� � ������ ��� �������
				if (treeId[v1] != treeId[v2]) {
					tree->Add(v1);
					tree->Add(v2);

					int oldId = treeId[v2]; // ���������� ���������� �������� ������� ������
					int newId = treeId[v1]; // ���������� ����� �������� �������

											// �������� ������� ��������� ������� �� �����
					for (int j = 0; j < vertices->Count; j++)
						if (treeId[j] == oldId)
							treeId[j] = newId;
				}
			}

			DrawTree(tree, "�������� ��������", compares);
		}

		~Form1() {
			if (components) {
				delete components;
			}
		}

	private: System::Windows::Forms::PictureBox^  Canvas;
	protected:
	private: System::Windows::Forms::DataGridView^  EdgeGrid;
	private: System::Windows::Forms::MenuStrip^  menuStrip1;
	private: System::Windows::Forms::ToolStripMenuItem^  PrimItem;
	private: System::Windows::Forms::ToolStripMenuItem^  KruskalItem;

	private:
		System::ComponentModel::Container ^components;

#pragma region Windows Form Designer generated code
		void InitializeComponent(void) {
			System::Windows::Forms::DataGridViewCellStyle^  dataGridViewCellStyle1 = (gcnew System::Windows::Forms::DataGridViewCellStyle());
			this->Canvas = (gcnew System::Windows::Forms::PictureBox());
			this->EdgeGrid = (gcnew System::Windows::Forms::DataGridView());
			this->v1 = (gcnew System::Windows::Forms::DataGridViewTextBoxColumn());
			this->v2 = (gcnew System::Windows::Forms::DataGridViewTextBoxColumn());
			this->length = (gcnew System::Windows::Forms::DataGridViewTextBoxColumn());
			this->menuStrip1 = (gcnew System::Windows::Forms::MenuStrip());
			this->PrimItem = (gcnew System::Windows::Forms::ToolStripMenuItem());
			this->KruskalItem = (gcnew System::Windows::Forms::ToolStripMenuItem());
			this->statusStrip1 = (gcnew System::Windows::Forms::StatusStrip());
			this->toolStripStatusLabel1 = (gcnew System::Windows::Forms::ToolStripStatusLabel());
			this->ResBox = (gcnew System::Windows::Forms::RichTextBox());
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->Canvas))->BeginInit();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->EdgeGrid))->BeginInit();
			this->menuStrip1->SuspendLayout();
			this->statusStrip1->SuspendLayout();
			this->SuspendLayout();
			// 
			// Canvas
			// 
			this->Canvas->Anchor = static_cast<System::Windows::Forms::AnchorStyles>((((System::Windows::Forms::AnchorStyles::Top | System::Windows::Forms::AnchorStyles::Bottom)
				| System::Windows::Forms::AnchorStyles::Left)
				| System::Windows::Forms::AnchorStyles::Right));
			this->Canvas->Location = System::Drawing::Point(12, 33);
			this->Canvas->Name = L"Canvas";
			this->Canvas->Size = System::Drawing::Size(635, 437);
			this->Canvas->TabIndex = 0;
			this->Canvas->TabStop = false;
			this->Canvas->MouseClick += gcnew System::Windows::Forms::MouseEventHandler(this, &Form1::Canvas_MouseClick);
			this->Canvas->MouseMove += gcnew System::Windows::Forms::MouseEventHandler(this, &Form1::Canvas_MouseMove);
			// 
			// EdgeGrid
			// 
			this->EdgeGrid->AllowUserToAddRows = false;
			this->EdgeGrid->AllowUserToDeleteRows = false;
			this->EdgeGrid->AllowUserToResizeColumns = false;
			this->EdgeGrid->AllowUserToResizeRows = false;
			this->EdgeGrid->Anchor = static_cast<System::Windows::Forms::AnchorStyles>(((System::Windows::Forms::AnchorStyles::Top | System::Windows::Forms::AnchorStyles::Bottom)
				| System::Windows::Forms::AnchorStyles::Right));
			this->EdgeGrid->ColumnHeadersHeightSizeMode = System::Windows::Forms::DataGridViewColumnHeadersHeightSizeMode::AutoSize;
			this->EdgeGrid->Columns->AddRange(gcnew cli::array< System::Windows::Forms::DataGridViewColumn^  >(3) {
				this->v1, this->v2,
					this->length
			});
			this->EdgeGrid->Location = System::Drawing::Point(653, 33);
			this->EdgeGrid->Name = L"EdgeGrid";
			this->EdgeGrid->RowHeadersVisible = false;
			this->EdgeGrid->Size = System::Drawing::Size(153, 298);
			this->EdgeGrid->TabIndex = 1;
			this->EdgeGrid->CellValueChanged += gcnew System::Windows::Forms::DataGridViewCellEventHandler(this, &Form1::EdgeGrid_CellValueChanged);
			this->EdgeGrid->KeyDown += gcnew System::Windows::Forms::KeyEventHandler(this, &Form1::EdgeGrid_KeyDown);
			// 
			// v1
			// 
			this->v1->AutoSizeMode = System::Windows::Forms::DataGridViewAutoSizeColumnMode::Fill;
			dataGridViewCellStyle1->Alignment = System::Windows::Forms::DataGridViewContentAlignment::TopCenter;
			this->v1->DefaultCellStyle = dataGridViewCellStyle1;
			this->v1->HeaderText = L"v1";
			this->v1->Name = L"v1";
			this->v1->Resizable = System::Windows::Forms::DataGridViewTriState::False;
			this->v1->SortMode = System::Windows::Forms::DataGridViewColumnSortMode::NotSortable;
			// 
			// v2
			// 
			this->v2->AutoSizeMode = System::Windows::Forms::DataGridViewAutoSizeColumnMode::Fill;
			this->v2->HeaderText = L"v2";
			this->v2->Name = L"v2";
			// 
			// length
			// 
			this->length->AutoSizeMode = System::Windows::Forms::DataGridViewAutoSizeColumnMode::Fill;
			this->length->HeaderText = L"�����";
			this->length->Name = L"length";
			// 
			// menuStrip1
			// 
			this->menuStrip1->Items->AddRange(gcnew cli::array< System::Windows::Forms::ToolStripItem^  >(2) { this->PrimItem, this->KruskalItem });
			this->menuStrip1->Location = System::Drawing::Point(0, 0);
			this->menuStrip1->Name = L"menuStrip1";
			this->menuStrip1->Size = System::Drawing::Size(818, 24);
			this->menuStrip1->TabIndex = 2;
			this->menuStrip1->Text = L"menuStrip1";
			// 
			// PrimItem
			// 
			this->PrimItem->Name = L"PrimItem";
			this->PrimItem->Size = System::Drawing::Size(115, 20);
			this->PrimItem->Text = L"�������� �����";
			this->PrimItem->Click += gcnew System::EventHandler(this, &Form1::PrimItem_Click);
			// 
			// KruskalItem
			// 
			this->KruskalItem->Name = L"KruskalItem";
			this->KruskalItem->Size = System::Drawing::Size(128, 20);
			this->KruskalItem->Text = L"�������� ��������";
			this->KruskalItem->Click += gcnew System::EventHandler(this, &Form1::KruskalItem_Click);
			// 
			// statusStrip1
			// 
			this->statusStrip1->Items->AddRange(gcnew cli::array< System::Windows::Forms::ToolStripItem^  >(1) { this->toolStripStatusLabel1 });
			this->statusStrip1->Location = System::Drawing::Point(0, 473);
			this->statusStrip1->Name = L"statusStrip1";
			this->statusStrip1->Size = System::Drawing::Size(818, 22);
			this->statusStrip1->SizingGrip = false;
			this->statusStrip1->TabIndex = 3;
			this->statusStrip1->Text = L"statusStrip1";
			// 
			// toolStripStatusLabel1
			// 
			this->toolStripStatusLabel1->Name = L"toolStripStatusLabel1";
			this->toolStripStatusLabel1->Size = System::Drawing::Size(0, 17);
			// 
			// ResBox
			// 
			this->ResBox->Anchor = static_cast<System::Windows::Forms::AnchorStyles>((System::Windows::Forms::AnchorStyles::Bottom | System::Windows::Forms::AnchorStyles::Right));
			this->ResBox->BorderStyle = System::Windows::Forms::BorderStyle::FixedSingle;
			this->ResBox->Location = System::Drawing::Point(653, 337);
			this->ResBox->Name = L"ResBox";
			this->ResBox->Size = System::Drawing::Size(153, 133);
			this->ResBox->TabIndex = 4;
			this->ResBox->Text = L"";
			// 
			// Form1
			// 
			this->AutoScaleDimensions = System::Drawing::SizeF(6, 13);
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->ClientSize = System::Drawing::Size(818, 495);
			this->Controls->Add(this->ResBox);
			this->Controls->Add(this->statusStrip1);
			this->Controls->Add(this->EdgeGrid);
			this->Controls->Add(this->Canvas);
			this->Controls->Add(this->menuStrip1);
			this->MainMenuStrip = this->menuStrip1;
			this->Name = L"Form1";
			this->Text = L"������ �����-��������";
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->Canvas))->EndInit();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->EdgeGrid))->EndInit();
			this->menuStrip1->ResumeLayout(false);
			this->menuStrip1->PerformLayout();
			this->statusStrip1->ResumeLayout(false);
			this->statusStrip1->PerformLayout();
			this->ResumeLayout(false);
			this->PerformLayout();

		}
#pragma endregion
};
}